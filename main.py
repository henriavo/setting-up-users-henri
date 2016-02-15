#!/usr/bin/env python
#
form = """
<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(aUserName)s">
          </td>
          <td class="error">
            %(one)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(two)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(three)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(anEmail)s">
          </td>
          <td class="error">
            %(four)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

welcomeForm = """
<form> method="get" action="/welcome">
	<p name="username" ><b>Welcome, %s !</b>.</p>
</form>

"""

import webapp2
import re

class MainHandler(webapp2.RequestHandler):

	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASSWORD_RE = re.compile(r"^.{3,20}$")
	EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


	def get(self):
		self.writeForm()


	def writeForm(self, message={"one": "",
              "two": "",
              "three": "",
              "four": "",
              "aUserName":"",
              "anEmail":""}):
		self.response.write(form % message)

	def post(self):
		errorMsg = {"one": "",
              "two": "",
              "three": "",
              "four": "",
              "aUserName":"",
              "anEmail":""}

		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		errorFound = False

		if(self.verifyUsername(username)):
			pass
		else:
			errorFound = True
			errorMsg['one'] = "That's not a valid username"
			errorMsg['aUserName'] = username
			errorMsg['anEmail'] = email

		if(self.verifyPass(password)):
			pass
		else:
			errorFound = True
			errorMsg['two'] = "That's not a valid password"
			errorMsg['aUserName'] = username
			errorMsg['anEmail'] = email

		if(password == verify):
			pass
		else:
			errorFound = True
			errorMsg['three'] = "Your passwords didn't match"
			errorMsg['aUserName'] = username
			errorMsg['anEmail'] = email

		if(self.verifyEmail(email)):
			pass
		else:
			errorFound = True
			errorMsg['four'] = "That's not a valid email."
			errorMsg['aUserName'] = username
			errorMsg['anEmail'] = email

		#determine how to respond
		if(errorFound == False):
			print "DICTIONARY: %s" % errorMsg.items()
			self.redirect("/welcome?username=%s" % username)
			
		else:
			print "DICTIONARY: %s" % errorMsg.items()
			self.writeForm(errorMsg)

	def verifyUsername(self, username):
		return self.USER_RE.match(username)

	def verifyPass(self, password):
		return self.PASSWORD_RE.match(password)

	def verifyEmail(self, email):
		return self.EMAIL_RE.match(email)


class WelcomeHandler(webapp2.RequestHandler): 
	def get(self):
		verifiedUserName = self.request.get('username')
		self.response.write("<b>Welcome, %s!<b>" % verifiedUserName)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',WelcomeHandler)
], debug=True)
