import sqlite3
from datetime import datetime
import FileManager
import ServerConfigurator

config = ServerConfigurator.get_configure()


def connect_DB(commit=False):
    connection = sqlite3.connect(config["DB_path"])
    if not commit:
        cursor = connection.cursor()
        return cursor
    else:
        return connection


def update_DB(dateupdate=None, dateadd=None, datedelete=None):
    connection = connect_DB(True)
    cursor = connection.cursor()
    if dateupdate:
        for update in dateupdate:
            cursor.execute(
                f"""UPDATE {config['files_table']} SET time = "{update[1]}" WHERE filename = "{update[0]}" """)
    if dateadd:
        for add in dateadd:
            cursor.execute(f"""INSERT INTO {config['files_table']}(filename, time) VALUES("{add[0]}", "{add[1]}") """)
    if datedelete:
        for delete in datedelete:
            cursor.execute(f"""UPDATE {config['files_table']} SET status = "DELETED" WHERE filename = "{delete}"  """)
    connection.commit()


def return_update_statement(files: dict):
    cursor = connect_DB()
    result = dict()
    redact_time = dict()
    for line in list(cursor.execute(f"""SELECT filename, time, status FROM  {config['files_table']}""").fetchall()):
        redact_time[line[0]] = (line[1], line[2])

    for file in redact_time.keys():
        if not files and redact_time[file][1] == "UPDATED":
            result[file] = "UPDATE"
        elif file in files.keys():
            if redact_time[file][1] == "UPDATED" and datetime.strptime(redact_time[file][0],
                                                                       "%y-%m-%d") >= datetime.strptime(files[file],
                                                                                                        "%y-%m-%d"):
                result[file] = "UPDATE"

        elif redact_time[file][1] == "UPDATED" and file not in files.keys():
            result[file] = "UPDATE"
        elif redact_time[file][1] == "DELETED":
            result[file] = "DELETE"
    cursor.close()
    return result


def DB_sync_files():
    cursor = connect_DB()
    redact_time = dict()
    files = FileManager.get_server_files()
    for line in list(cursor.execute(f"""SELECT filename, time FROM  {config['files_table']}""").fetchall()):
        redact_time[line[0]] = line[1]

    dateupdate = []
    dateadd = []
    datedelete = []

    for file in files.keys():
        if file in redact_time.keys():
            if str(redact_time[file]) != str(files[file]):
                dateupdate.append([file, files[file]])
            redact_time.pop(file)
        else:
            dateadd.append([file, files[file]])
    if redact_time:
        datedelete.append(*redact_time.keys())
    update_DB(dateupdate, dateadd, datedelete)
