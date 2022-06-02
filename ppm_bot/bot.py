import requests
from bs4 import BeautifulSoup


def content_length(data):
    length = 1
    for key, value in data.items():
        length += len(str(key))
        length += len(str(value))
        if len(str(value)) != 0:
            length += 2
        else:
            length += 1
    return length


class Bot:
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en,q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
        }
        self.players = []
        self.session = requests.session()
        self.update_headers()

    def login(self, username, password):
        # Create data
        data = {"lng": "sk", "username": username, "password": password}

        # Add headers
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.headers["Content-Length"] = str(content_length(data))
        self.update_headers()

        # Send login request
        response = self.session.post(
            "https://www.powerplaymanager.com/action/action_ams_user_login.php",
            data=data,
        )

        # Remove headers
        self.headers.pop("Content-Length")
        self.headers.pop("Content-Type")
        self.update_headers()

        # Check if login was successful
        return response.status_code == 200 and len(response.history) == 1

    def logout(self):
        response = self.session.get("https://www.powerplaymanager.com/action/action_ams_user_logout.php?lng=sk")
        return response.status_code == 200

    def find_players(self):
        self.players = []
        # Get table with players stats
        response = self.session.get("https://hockey.powerplaymanager.com/sk/trening-hracov.html")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "lxml")
            table = soup.find("table", class_="table")

            # Find players
            for tr in table.find_all("tr"):
                p_id = tr.find("select")
                if p_id is not None:
                    p_id = p_id["name"]
                    name = tr.find("a", class_="link_name").text
                    player = Player(name, p_id)

                    # Find player's attributes
                    attrs = []
                    qualities = []
                    for td in tr.find_all("td"):
                        span = td.find("span", class_="kva")
                        if span is not None:
                            qualities.append(span.text)
                            span.decompose()
                            attrs.append(td.text)
                    player.set_attrs(attrs)
                    player.set_qualities(qualities)
                    self.players.append(player)
        self.find_player_types()
        return self.players

    def set_player_type(self, player, p_type):
        player.set_type(p_type)
        file = open("player_types.txt", "w")
        for player in self.players:
            if player.type is not None:
                file.write(player.id + " " + player.type + "\n")
        file.close()

    def find_player_types(self):
        try:
            file = open("player_types.txt", "r")
        except FileNotFoundError:
            open("player_types.txt", "w").close()
            file = open("player_types.txt", "r")
        for line in file:
            line = line.strip().split()
            player = self.get_player(line[0])
            if player is not None:
                player.set_type(line[1])

    def get_player(self, p_id):
        for player in self.players:
            if player.id == p_id:
                return player

    def train_players(self, ratios):
        # Update players
        self.find_players()

        # Get data for training
        data = {}
        for player in self.players:
            if player.type is None:
                data[player.id] = 0
            else:
                data[player.id] = player.train(ratios[player.type])

        # Add headers
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.headers["Content-Length"] = str(content_length(data))
        self.update_headers()

        # Send request
        response = self.session.post("https://hockey.powerplaymanager.com/sk/trening-hracov.html", data=data)
        if response.status_code == 200:
            self.headers.pop("Content-Length")
            self.headers.pop("Content-Type")
            self.update_headers()
            return True
        return False

    def update_headers(self):
        # Add "Cookie" value to headers
        cookies = self.session.cookies.get_dict()
        h_cookies = []
        for key in cookies.keys():
            h_cookies.append(key + "=" + cookies[key])
        if h_cookies:
            self.headers["Cookie"] = "; ".join(h_cookies)
        self.session.headers.clear()
        self.session.headers.update(self.headers)


class Player:
    def __init__(self, p_name, p_id):
        self.name = p_name
        self.id = p_id
        self.type = None
        self.attributes = []
        self.qualities = []

    def set_attrs(self, attrs):
        for attr in attrs:
            self.attributes.append(int(attr))

    def set_qualities(self, qualities):
        for qual in qualities:
            self.qualities.append(int(qual))

    def set_type(self, p_type):
        self.type = p_type

    def train(self, ratio):
        if len(self.attributes) != 7:
            return 0
        min_i = ratio.index(max(ratio))
        for i in range(len(self.attributes)):
            if ratio[i] == 0:
                ratio[i] = 0.001
            if self.attributes[i] / ratio[i] < self.attributes[min_i] / ratio[min_i]:
                min_i = i
        return min_i + 1

    def __str__(self):
        attributes = []
        if len(self.attributes) == 7 and len(self.qualities) == 7:
            for i in range(7):
                attributes.append(str(self.attributes[i]) + "/" + str(self.qualities[i]))
        else:
            attributes = ["0/0"] * 7
        return self.id + " " + str(self.type) + " " + self.name + " " + " ".join(attributes)
