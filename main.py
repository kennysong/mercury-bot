import cgi
import jinja2
import os
import webapp2

from google.appengine.ext import db
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import xmpp_handlers

## end imports ##

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

## end templates ##

def get_user(gmail):
    q = User.all().filter('gmail =', gmail)
    user = q.get()
    if not user:
    	user = User(gmail=gmail, websites=[])
    	user.put()
    return user

## end controllers ##

class User(db.Model):
	gmail = db.StringProperty(required = True)
	websites = db.StringListProperty(required = True)

## end models ##

class BaseHandler(webapp2.RequestHandler):
	def write(self, x):
		return self.response.out.write(x)
	def rget(self, x):
		return self.request.get(x)
	def render(self, template, params={}):
		template = jinja_env.get_template(template)
		self.response.out.write(template.render(params))

class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        sender = cgi.escape(self.request.get('from')).split("/")[0]
        body = message.body

        user = get_user(sender)

        if body == 'ls' or body == 'list':
        	s = ''
        	for site in user.websites:
        		if not site: continue
        		s += site + '<br />'
        	message.reply(s)

        elif 'http://' in body:
        	user.websites.append(body)
        	user.put()
        	message.reply('Added!')

        else:
        	message.reply('I didn\'t understand that.')

class HomeHandler(BaseHandler):
	def get(self):
		pass

## end handlers ##
 
app = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)
 
def main():
    run_wsgi_app(app)
 
if __name__ == "__main__":
    main()