import cgi

import webapp2

rot13_form = """
<form method="post" action="/rot13">
    <h1>Enter some text to ROT13</h1>
    <textarea name="text">%(rot13text)s</textarea>
    <input type="submit">
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


app = webapp2.WSGIApplication([
    ('/rot13', Rot13),
], debug=True)
