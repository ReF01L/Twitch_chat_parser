import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

HOST = config["Twitch"]["host"]
PORT = int(config["Twitch"]["port"])
NICK = config["Twitch"]["nick"]
PASS = config["Twitch"]["pass"]
CHAN = config["Twitch"]["chan"]


def swap_channel(value):
    config.set("Twitch", "chan", value)
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
