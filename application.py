# -*- coding:utf-8 -*-
import os
import sys
import time
import base64
import sqlite3
import configparser

import tornado.web
import tornado.httpserver
from tornado.web import URLSpec


handlers = list()
setting = dict(
    compress_response = True,
    static_path = os.path.join(os.getcwd(), "static"),
    template_path = os.path.join(os.getcwd(), "template"),
    xsrf_cookies = True,
    debug = True,
    cookie_secret = "919547850f4e497887d4e0d22a67e8a0",
    login_url = "/login",
    static_url_prefix = "/static/",
    static_handler_args = dict(default_filename="index.html")  # 当一个目录被请求时，自动地伺服index.html文件
)
config = configparser.ConfigParser()
print("Reading configuration from: {0}".format(config.read("conf" + os.sep + "config.ini")))

db = sqlite3.connect("tornadoUser.db")


class BaseHandler(tornado.web.RequestHandler):
    # 所有 RequestHandler 的基类
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render("404.html")
        elif status_code == 500:
            self.render("500.html")
        elif status_code == 405:
            self.render("verboseNotAllowed.html")
        else:
            self.write("Error: {0}".format(status_code))
    
    def get_current_user(self):
        # 返回类型str 或者NoneType
        userName = self.get_secure_cookie('userName')
        if isinstance(userName, bytes):
            return userName.decode(encoding='utf-8')
        return None

class EntryHandler(BaseHandler):
    """只有被认证成功的用户才会被重定向到/welcome，否则定向到login_url指定的路径"""
    @tornado.web.authenticated
    def get(self):
        self.redirect("/welcome")


class RegisterHandler(BaseHandler):
    def initialize(self, db):
        self.db = db
    
    def prepare(self):
        # 分配一个数据库操作光标
        self.cursor = self.db.cursor()
    
    def get(self):
        self.render("register.html")
    
    def post(self):
        userName = self.get_argument("userName", None)
        passWord = self.get_argument("passWord", None)
        print(userName, passWord)
        if all((userName, passWord)):
            sql = "SELECT username FROM login WHERE username=?"
            beforeRegQueryResult = self.cursor.execute(sql, (userName,))  # 返回int类型
            if beforeRegQueryResult:
                kwargs = dict()
                kwargs["userName"] = userName
                self.render("duplicatedRegisterUser.html", **kwargs)
            else:
                sql = "INSERT INTO login(username, password) VALUES(?, ?)"
                try:
                    insertResult = self.cursor.execute(sql, (userName, passWord))
                    if insertResult:
                        self.set_secure_cookie("userName", userName,
                                               expires=time.time() + 6 * 60 * 60)
                        self.redirect("/welcome")
                except Exception:
                    self.redirect("/wrong")
        else:
            self.redirect("/wrong")
    
    def on_finish(self):
        self.cursor.close()


class HelpHandler(BaseHandler):
    def get(self):
        self.render("help.html")

class LoginHandler(BaseHandler):
    def initialize(self, db):
        self.db = db
    
    def prepare(self):
        # 分配一个数据库操作光标
        self.cursor = self.db.cursor()
    
    def get(self):
        self.set_header("Content-Type", "text/html")
        self.render("login.html")
    
    def post(self):
        userName = self.get_argument('userName', default=None, strip=True)
        passWord = self.get_argument('passWord', default=None, strip=True)
        print("userName: {0}".format(userName))
        print("passWord: {0}".format(passWord))
        if not all((userName, passWord)):
            self.redirect("/login", permanent=False)
        else:
            sql = "SELECT username, password FROM login WHERE username=? AND password=?"
            self.cursor.execute(sql, (userName, passWord))
            if len(self.cursor.fetchall()) == 1:
                self.set_secure_cookie("userName", userName, expires=time.time() + 6 * 60 * 60)
                self.redirect("/welcome")
            else:
                self.redirect("/login", permanent=False)
    
    def on_finish(self):
        self.cursor.close()

class WelcomeHandler(BaseHandler):
    def prepare(self):
        pass
    
    def get(self):
        userName = self.current_user
        if isinstance(userName, str):
            kwargs = dict()
            kwargs["userName"] = userName
            # print("self.current_user: {0}".format(self.current_user))
            self.render("welcome.html", **kwargs)
        else:
            self.set_header("Content-Type", "text/html")
            self.redirect("/login")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")


class WrongHandler(BaseHandler):
    def get(self):
        self.render("wrong.html")

handlers.extend([
    URLSpec(r"/", EntryHandler, name="enterPoint"),
    URLSpec(r"/register", RegisterHandler, dict(db=db), name="registerHandler"),
    URLSpec(r"/help", HelpHandler, name="helpHandler"),
    URLSpec(r"/login", LoginHandler, dict(db=db), name="loginHandler"),
    URLSpec(r"/welcome", WelcomeHandler, name="welcomeHandler"),
    URLSpec(r"/logout", LogoutHandler, name="logoutHandler"),
    URLSpec(r"/wrong", WrongHandler, name="wrongHandler")
])

app = tornado.web.Application(
    handlers = handlers,
    **setting
)
