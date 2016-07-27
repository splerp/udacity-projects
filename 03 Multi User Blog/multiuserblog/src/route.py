import os
import webapp2
import jinja2

import security

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                        autoescape=True)

# Base handler for easier writing
class Handler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params, name=self.request.get("name"))
        
    def render(self, template, must_be_logged_in = False, **kw):
    
        # Append data that should be available on all pages.
        kw['user_name'] = security.cookie_value(self.request.cookies.get('user_name', None))
        
        if must_be_logged_in and not security.is_logged_in(self.request):
            self.write(self.render_str("403.html", **kw))
        else:
            self.write(self.render_str(template, **kw))
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def getThese(self, *names):
        
        values = []
        for name in names:
            values.append(self.request.get(name))
        
        return tuple(values)
