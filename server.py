import tornado.ioloop
import tornado.web

import base64
import uuid

import config

cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

class HomeHandler(tornado.web.RequestHandler):
	def get(self):
		if self.get_secure_cookie("username"):
			return self.write(config.MESSAGE)
		else:
			self.redirect("/")

class RootHandler(tornado.web.RequestHandler):
	def get(self):
		# if not self.get_secure_cookie("username"):
		# 	return self.render("templates/index.html", error=None)
		# else:
		# 	self.redirect("/home")
		self.render("templates/index.html", error=None)

	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		if username == config.USERNAME and password == config.PASSWORD:
			self.set_secure_cookie("username", username)
			self.redirect("/home")
		else:
			self.render("templates/index.html", error="Login failed")


application = tornado.web.Application([
	(r'/home', HomeHandler),
	(r'/', RootHandler),
	(r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': 'static/'}),
	(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
], cookie_secret=cookie_secret)

if __name__ == "__main__":
	application.listen(80)
	tornado.ioloop.IOLoop.instance().start()

