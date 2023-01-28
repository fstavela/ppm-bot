import csv
import random
from collections import OrderedDict
from os.path import exists
from time import sleep

from bot import Bot
from config_loader import load_config


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
        "C": [0, 0, 100, 80, 50, 50, 0],
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


def get_finances(bot):
    finances = bot.get_finances()
    for sport, finance in finances.items():
        current_data = OrderedDict()
        for date in (bot.today, bot.yesterday):
            current_data[date.isoformat()] = finance["income"][date] + finance["payments"][date]
        current_data[bot.today.isoformat()] += [finance["balance"]["today"], finance["balance"]["total"]]
        current_data[bot.yesterday.isoformat()] += [finance["balance"]["yesterday"]]

        file_name = f"finance_{sport}.csv"

        if not exists(file_name):
            new_file = open(file_name, "w")
            new_file.close()

        with open(file_name, "r", newline="") as rfile:
            reader = csv.reader(rfile)
            for row in reader:
                if row[0] not in current_data:
                    current_data[row[0]] = row[1:]

        with open(file_name, "w", newline="") as wfile:
            writer = csv.writer(wfile)
            for date, data in current_data.items():
                writer.writerow([date] + data)


config = load_config()
logged = False
hockey_bot = Bot(config["lng"])

login(hockey_bot, config["username"], config["password"])
sleep(random.randint(4000, 6000) / 1000)
get_finances(hockey_bot)
sleep(random.randint(4000, 6000) / 1000)
logout(hockey_bot)


# while True:
#     action = input("Command: ")
#     if action.lower() == "login":
#         if not logged:
#             username = input("Username: ")
#             password = input("Password: ")
#             if login(hockey_bot, username, password):
#                 logged = True
#             time.sleep(random.randint(4000, 6000) / 1000)
#         else:
#             print("You are already logged in")
#     elif action.lower() == "train":
#         if logged:
#             train(hockey_bot)
#             time.sleep(random.randint(4000, 6000) / 1000)
#         else:
#             print("You are not logged in")
#     elif action.lower() == "settype":
#         set_type(hockey_bot)
#     elif action.lower() == "players":
#         if logged:
#             find_players(hockey_bot)
#             time.sleep(random.randint(4000, 6000) / 1000)
#         else:
#             print("You are not logged in")
#     elif action.lower() == "logout":
#         if logged:
#             logout(hockey_bot)
#             logged = False
#         else:
#             print("You are not logged in")
#     elif action.lower() == "exit":
#         if logged:
#             logout(hockey_bot)
#             logged = False
#         exit()
#     elif action.lower() == "finance":
#         if logged:
#             scrape_finance(hockey_bot)
#             time.sleep(random.randint(4000, 6000) / 1000)
#         else:
#             print("You are not logged in")
#     else:
#         print("Unknown command:", action)
