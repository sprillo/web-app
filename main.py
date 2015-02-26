import webapp2

######################### Jinja Scaffold ###############################

import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)
	
	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)
	
	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))


################################ / #####################################

class MainPage(Handler):
    def get(self):
        self.render("root.html")

##################  olympiad-problem-classifier ########################

import classifier

class Olympiad_problem_classifier(Handler):
	def get(self):
		self.render("olympiad_problem_classifier.html",
					statement = "Every even integer greater than 2 can be expressed as the sum of two primes.",
					message = [""])
	def post(self):
		statement = self.request.get("statement")
		message = classifier.classify_statement(statement)
		self.render("olympiad_problem_classifier.html",statement = statement, message = message)

############################ Handlers ##################################

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/olympiad_problem_classifier',Olympiad_problem_classifier)
], debug=True)

########################################################################