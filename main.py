import cgi

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
    <div>Name: <input title="Please, provide your name" type="text" name="username" placeholder="John Doe"><span style="color: red">%(username_error)s</span></div>
    <div>Password: <input title="Please, provide a strong password" type="password" name="password"><span style="color: red">%(password_error)s</span></div>
    <div>Verify passowrd: <input title="Please, verify your password" type="password" name="verify"><span style="color: red">%(verify_error)s</span></div>
    <div>Your email: <input title="Please, provide your email address" type="email" name="email" placeholder="your@email.com"><span style="color: red">%(email_error)s</span></div>
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
        self.redirect("/welcome")

    def write_form(self, username_error="", password_error="", verify_pass_error="", email_error=""):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(signup_form % {
            "username_error": username_error,
            "password_error": password_error,
            "verify_error": verify_pass_error,
            "email_error": email_error
        })


class Welcome(webapp2.RequestHandler):
    def get(self):
        return self.response.out.write("Welcome")


app = webapp2.WSGIApplication([
    ('/rot13', Rot13),
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)
