import DBManager
import ServerConfigurator

config = ServerConfigurator.get_configure()


def check_valid_login(username, password):
    cursor = DBManager.connect_DB()
    result = cursor.execute(
        f"""SELECT id FROM {config["user_tablet"]} WHERE username = "{username}" AND password = {password}""").fetchall()

    if result:
        return True
    return False


def check_admin_login(username, password):
    cursor = DBManager.connect_DB()
    request = cursor.execute(
        f"""SELECT role FROM {config["user_tablet"]} WHERE username = "{username}" AND password = {password}""").fetchone()
    if request[0] == "ADMIN":
        return True
    else:
        return False
