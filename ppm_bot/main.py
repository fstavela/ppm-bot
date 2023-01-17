import random
import time

from bot import Bot

from ppm_bot.config_loader import load_config


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


config = load_config()
logged = False
hockey_bot = Bot()

while True:
    action = input("Command: ")
    if action.lower() == "login":
        if not logged:
            username = input("Username: ")
            password = input("Password: ")
            if login(hockey_bot, username, password):
                logged = True
            time.sleep(random.randint(4000, 6000) / 1000)
        else:
            print("You are already logged in")
    elif action.lower() == "train":
        if logged:
            train(hockey_bot)
            time.sleep(random.randint(4000, 6000) / 1000)
        else:
            print("You are not logged in")
    elif action.lower() == "settype":
        set_type(hockey_bot)
    elif action.lower() == "players":
        if logged:
            find_players(hockey_bot)
            time.sleep(random.randint(4000, 6000) / 1000)
        else:
            print("You are not logged in")
    elif action.lower() == "logout":
        if logged:
            logout(hockey_bot)
            logged = False
        else:
            print("You are not logged in")
    elif action.lower() == "exit":
        if logged:
            logout(hockey_bot)
            logged = False
        exit()
    else:
        print("Unknown command:", action)
