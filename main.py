import webapp2

form ="""
<form method="post" action="/testform">
    <input name="q">
    <input type="submit">
</form>
"""


class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(form)


class TestHandler(webapp2.RequestHandler):
    def post(self):
        q = self.request.get("q")
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(q)


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    ('/testform', TestHandler)
], debug=True)
