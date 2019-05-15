from bot_classes import Bot
import time, random


def login(bot, username, password):
    if bot.login(username, password):
        print("Successfully logged in as " + username)
        return True
    print("Failed to log in as " + username)
    return False


def logout(bot):
    if bot.logout():
        print("Logged out")


def find_players(bot):
    players = bot.find_players()
    print("Players:")
    for player in players:
        print(player)


def train(bot):
    ratios = {
        "G": [100, 0, 0, 0, 50, 50, 0],
        "D": [0, 100, 0, 20, 50, 40, 50],
        "W": [0, 0, 100, 80, 0, 50, 50],
        "C": [0, 0, 100, 80, 50, 50, 0]
    }
    if bot.train_players(ratios):
        print("Training successfully set")
        return True
    return False


def set_type(bot):
    p_id = input("Player ID: ")
    p_type = input("Player type: ")
    player = bot.get_player(p_id)
    bot.set_player_type(player, p_type)


bot = Bot()
run = False

username = input("Username: ")
password = input("Password: ")

if login(bot, username, password):
    run = True
    time.sleep(random.randint(4000, 6000) / 1000)
    find_players(bot)
    time.sleep(random.randint(4000, 6000) / 1000)

while run:
    action = input("Command: ")
    if action.lower() == "train":
        train(bot)
        time.sleep(random.randint(4000, 6000) / 1000)
    if action.lower() == "settype":
        set_type(bot)
    if action.lower() == "players":
        find_players(bot)
        time.sleep(random.randint(4000, 6000) / 1000)
    if action.lower() == "logout":
        logout(bot)
        run = False
