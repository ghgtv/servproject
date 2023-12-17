import json


def get_configure():
    jsonfile = open("ServerConfig.json", "r")
    config = json.load(jsonfile)
    jsonfile.close()
    return config
