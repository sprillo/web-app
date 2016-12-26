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

#########################  AutoTabber ##################################

import autoTabber

class Auto_tabber(Handler):
	def get(self):
		self.render("auto_tabber.html",
					stringNotes = "D7 G5 B5 e5 D6e7 B5 G5 e7 D5e8 B5 G5 e8 D4e2 B3 G2 e2 D3e0 B1 G2 B1 e0 B1 G2 A2G0B0 A0G2B1 A0G2B1",
					phrasePenalty = "10",
					pinkyPenalty = "1",
					message = [""])
	def post(self):
		stringNotes = self.request.get("stringNotes")
		phrasePenalty = self.request.get("phrasePenalty")
		pinkyPenalty = self.request.get("pinkyPenalty")
		print("phrasePenalty = %s"%phrasePenalty)
		print("pinkyPenalty = %s"%pinkyPenalty)
		message = autoTabber.autoTab(stringNotes,phrasePenalty,pinkyPenalty)
		self.render("auto_tabber.html",
					stringNotes = stringNotes,
					phrasePenalty = phrasePenalty,
					pinkyPenalty = pinkyPenalty,
					message = message)

######################### /robots.txt ##################################

class Robots(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.render("robots.html")

############################ Handlers ##################################

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/olympiad_problem_classifier',Olympiad_problem_classifier),
    ('/auto_tabber',Auto_tabber),
    ('/robots.txt',Robots)
], debug=True)

########################################################################
