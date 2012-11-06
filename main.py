import cgi
import jinja2
import os
import webapp2

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import xmpp_handlers

## end imports ##

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

## end templates ##

class BaseHandler(webapp.RequestHandler):
	def write(self, x):
		return self.response.out.write(x)
	def rget(self, x):
		return self.request.get(x)

class XMPPHandler(BaseHandler):
    def post(self):
    	message = xmpp.Message(self.request.POST)
        sender = cgi.escape(self.request.get('from')).split("/")[0]
        body = message.body
        message.reply("Hello, " + sender + "!, you sent: " + message.body)


app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              debug=True)