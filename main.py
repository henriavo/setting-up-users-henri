#!/usr/bin/env python
#

import webapp2
import re
import os
import jinja2
import DbDefinitions
import PasswordHash

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kwArgs):
        self.response.write(*a, **kwArgs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def renderIt(self, template, **kwArgs):
        self.write(self.render_str(template, **kwArgs))


class MainHandler(Handler):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    def get(self):
        self.writeForm()

    def writeForm(self, message={"one": "",
                                 "two": "",
                                 "three": "",
                                 "four": "",
                                 "aUserName": "",
                                 "anEmail": ""}):

        self.renderIt("form.html", one=message.get("one"),
                                    two=message.get("two"),
                                    three=message.get("three"),
                                    four=message.get("four"),
                                    aUserName=message.get("aUserName"),
                                    anEmail=message.get("anEmail"))

    def post(self):
        errorMsg = {"one": "",
                    "two": "",
                    "three": "",
                    "four": "",
                    "aUserName": "",
                    "anEmail": ""}

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        errorFound = False

        errorFound = self.processUsername(email, errorFound, errorMsg, username)

        errorFound = self.processPassword(email, errorFound, errorMsg, password, username)

        errorFound = self.processPasswordMatch(email, errorFound, errorMsg, password, username, verify)

        errorFound = self.processEmail(email, errorFound, errorMsg, username)

        # determine how to respond
        if (errorFound == False):
            #HANDLE NEW USER,  hash and salt the password
            salt = PasswordHash.make_salt()
            passwordHash = PasswordHash.make_pw_hash(username,password,salt)


            newuser = DbDefinitions.User(username=username,password=passwordHash,email=email)
            newuser.put()
            print "THE ID: " + str(newuser.key().id())
            newuserDbId = str(newuser.key().id())

            self.redirect("/welcome/%s" % newuserDbId)



        else:
            self.writeForm(errorMsg)

    #helper method below

    def processEmail(self, email, errorFound, errorMsg, username):
        if (self.verifyEmail(email)):
            pass
        else:
            errorFound = True
            errorMsg['four'] = "That's not a valid email."
            errorMsg['aUserName'] = username
            errorMsg['anEmail'] = email

        return errorFound

    def processPasswordMatch(self, email, errorFound, errorMsg, password, username, verify):
        if (password == verify):
            pass
        else:
            errorFound = True
            errorMsg['three'] = "Your passwords didn't match"
            errorMsg['aUserName'] = username
            errorMsg['anEmail'] = email
        return errorFound

    def processPassword(self, email, errorFound, errorMsg, password, username):
        if (self.verifyPass(password)):
            pass
        else:
            errorFound = True
            errorMsg['two'] = "That's not a valid password"
            errorMsg['aUserName'] = username
            errorMsg['anEmail'] = email
        return errorFound

    def processUsername(self, email, errorFound, errorMsg, username):
        if (self.verifyUsername(username)):
            pass
        else:
            errorFound = True
            errorMsg['one'] = "That's not a valid username"
            errorMsg['aUserName'] = username
            errorMsg['anEmail'] = email
        return errorFound

    def verifyUsername(self, username):
        return self.USER_RE.match(username)

    def verifyPass(self, password):
        return self.PASSWORD_RE.match(password)

    def verifyEmail(self, email):
        return self.EMAIL_RE.match(email)


class WelcomeHandler(Handler):
    def get(self,newuser_id):

        auser = DbDefinitions.User.get_by_id(long(newuser_id))
        if auser:
            self.renderIt("welcomeForm.html", userName=auser.username)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome/([0-9]+)', WelcomeHandler)
], debug=True)
