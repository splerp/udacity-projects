import webapp2

class Handler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params, name=self.request.get("name"))
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class IndexHandler(Handler):
    def get(self):
        write("hi there")

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug=True)
