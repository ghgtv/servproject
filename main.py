from flask import Flask
from flask import request
from markupsafe import escape

import DBManager
import UserValidator
import FileManager

app = Flask(__name__)


@app.route("/")
def index():
    return "this server does not contain graphic information, please use direct POST/GET methods"


@app.route("/get_server_version", methods=["POST", "GET"])
def get_version_request():
    error = "this is version getter, send post request with username and password fields"
    if request.method == "POST":
        if UserValidator.check_valid_login(escape(request.form.get("username")), escape(request.form.get("password"))):
            return FileManager.send_version()

        else:
            error = "username/password don`t match, please check sending data fields"
    return error


@app.route("/get_server_files", methods=["POST", "GET"])
def get_files_request():
    error = "this is files getter, send post request with username and password fields"
    if request.method == "POST":
        if UserValidator.check_valid_login(escape(request.form.get("username")), escape(request.form.get("password"))):
            return FileManager.send_files(request.form.get("files_time"))
        else:
            error = "username/password don`t match, please check sending data fields"
    return error


@app.route("/update_db", methods=["POST", "GET"])
def update_DB():
    error = "Technical page for inner interactions, just leave it alone"
    if request.method == "POST":
        if UserValidator.check_valid_login(escape(request.form.get("username")),
                                           escape(request.form.get("password"))) and UserValidator.check_admin_login(
                escape(request.form.get("username")), escape(request.form.get("password"))):
            DBManager.DB_sync_files()
            return "Request approved"
        else:
            error = "YoU aRe NoT sUpPoSeD tO bE HeRe"
    return error


app.run(port=4567)
