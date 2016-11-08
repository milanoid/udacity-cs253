import cgi

import re
import webapp2

rot13_form = """
<form method="post" action="/rot13">
    <h1>Enter some text to ROT13</h1>
    <textarea name="text">%(rot13text)s</textarea>
    <input type="submit">
</form>
"""

signup_form = """
<h1>Signup form</h1 required="True">
<form method="post" action="/signup">
    <div>Name: <input title="Please, provide your name" type="text" name="username" value="%(username)s" placeholder="John Doe"><span style="color: red">%(username_error)s</span></div>
    <div>Password: <input title="Please, provide a strong password" type="password" name="password" value=""><span style="color: red">%(password_error)s</span></div>
    <div>Verify password: <input title="Please, verify your password" type="password" name="verify" value=""><span style="color: red">%(verify_error)s</span></div>
    <div>Your email: <input title="Please, provide your email address" type="text" name="email" value="%(email)s" placeholder="your@email.com"><span style="color: red">%(email_error)s</span></div>
    <button type="submit">Sign up</button>
</form>
"""


class Rot13(webapp2.RequestHandler):
    def get(self):
        self.response.write(self.write_form(form=rot13_form))

    def post(self):
        text = self.request.get("text")
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.write_form(form=rot13_form, rot13text=self.rot13(text=text)))

    def write_form(self, form, rot13text=""):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(form % {"rot13text": cgi.escape(rot13text, True)})

    def rot13(self, text):
        rot13_text = []
        for character in text:
            if character.isalpha():
                if character.isupper():
                    rot13_char = chr(ord(character) + 13)
                    if ord(rot13_char) > ord('Z'):
                        rot13_char = chr(ord(rot13_char) - 26)

                elif character.islower():
                    rot13_char = chr(ord(character) + 13)
                    if ord(rot13_char) > ord('z'):
                        rot13_char = chr(ord(rot13_char) - 26)
            else:
                rot13_char = character
            rot13_text.append(rot13_char)
        return "".join(rot13_text)


class Signup(webapp2.RequestHandler):

    def get(self):
        return self.write_form()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        password_verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = ""
        password_error = ""
        verify_pass_error = ""
        email_error = ""

        have_error = False

        is_username_valid = self.is_username_valid(username=username)
        is_password_valid = self.is_password_valid(password=password)
        is_password_verify_valid = self.is_password_verify_valid(password=password, password_verify=password_verify)
        is_email_valid = self.is_email_valid(email=email)

        if not is_username_valid:
            username_error = "Invalid username"
            have_error = True

        if not is_password_valid:
            password_error = "Invalid password"
            have_error = True

        if not is_password_verify_valid:
            verify_pass_error = "Passwords don't match"
            have_error = True

        if not is_email_valid:
            email_error = "Invalid email"
            have_error = True

        if have_error:
            self.write_form(
                username=username,
                email=email,
                username_error=username_error,
                password_error=password_error,
                verify_pass_error=verify_pass_error,
                email_error=email_error
            )
        else:
            self.redirect("/welcome?username=" + username)


    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    def is_username_valid(self, username):
        return username and self.USER_RE.match(username)

    PASS_RE = re.compile(r"^.{3,20}$")
    def is_password_valid(self, password):
        return password and self.PASS_RE.match(password)

    def is_password_verify_valid(self, password, password_verify):
        return password == password_verify

    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    def is_email_valid(self, email):
        return not email or self.EMAIL_RE.match(email)

    def write_form(self, username="", email="", username_error="", password_error="", verify_pass_error="", email_error=""):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(signup_form % {
            "username": username,
            "email": email,
            "username_error": username_error,
            "password_error": password_error,
            "verify_error": verify_pass_error,
            "email_error": email_error
        })


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        return self.response.out.write("Welcome, " + username)


app = webapp2.WSGIApplication([
    ('/rot13', Rot13),
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)
