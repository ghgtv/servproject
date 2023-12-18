import ServerConfigurator
import os.path
import DBManager
from datetime import datetime
import json

config = ServerConfigurator.get_configure()


def send_version():
    return config["files_version"]


def send_files(files_time):
    update = []
    delete = []

    files = DBManager.return_update_statement(json.loads(files_time))
    for file in files.keys():
        if files[file] == "UPDATE":
            f = open(file, mode="rb")
            update.append([file, str(f.read())])
            f.close()
        if files[file] == "DELETE":
            delete.append(file)
    result = {"UPDATE": update, "DELETE": delete, "EXE": f'{config["project_files"]}{config["exe_file"]}'}
    return result


def get_server_files():
    tempdict = dict()
    for address, dirs, files in os.walk(config["project_files"]):
        for name in files:
            tempdict[os.path.join(address, name)] = datetime.fromtimestamp(
                os.path.getmtime(os.path.join(address, name))).date()
    return tempdict
