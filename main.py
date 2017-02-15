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
					stringGuitarNotes = "D7 G5 B5 e5 D6e7 B5 G5 e7 D5e8 B5 G5 e8 D4e2 B3 G2 e2 D3e0 B1 G2 B1 e0 B1 G2 A2G0B0 A0G2B1 A0G2B1",
					wPinky = "1",
					wIndexFingerPosition = "0.1",
					wIsFretted = "1",
					wIFPDelta = "2",
					showFingerAnotations = "N",
					explainScore = "N",
					message = [""])
	def post(self):
		stringGuitarNotes = self.request.get("stringGuitarNotes")
		wPinky = self.request.get("wPinky")
		wIndexFingerPosition = self.request.get("wIndexFingerPosition")
		wIsFretted = self.request.get("wIsFretted")
		wIFPDelta = self.request.get("wIFPDelta")
		showFingerAnotations = self.request.get("showFingerAnotations")
		explainScore = self.request.get("explainScore")
		print("wPinky = %s"%wPinky)
		print("wIndexFingerPosition = %s"%wIndexFingerPosition)
		print("wIsFretted = %s"%wIsFretted)
		print("wIFPDelta = %s"%wIFPDelta)
		print("showFingerAnotations = %s"%showFingerAnotations)
		print("explainScore = %s"%explainScore)
		message = autoTabber.autoTab(stringGuitarNotes,wPinky,wIndexFingerPosition,wIsFretted,wIFPDelta)
		if showFingerAnotations == "N":
			message[1] = ""
		if explainScore == "N":
			message[2] = ""
		self.render("auto_tabber.html",
					stringGuitarNotes = stringGuitarNotes,
					wPinky = wPinky,
					wIndexFingerPosition = wIndexFingerPosition,
					wIsFretted = wIsFretted,
					wIFPDelta = wIFPDelta,
					showFingerAnotations = showFingerAnotations,
					explainScore = explainScore,
					message = message)
					
######################  AutoTabberSamples ##############################

import autoTabber

class Auto_tabber_samples(Handler):
	def get(self):
		self.render("auto_tabber_samples.html")

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
    ('/auto_tabber_samples',Auto_tabber_samples),
    ('/robots.txt',Robots)
], debug=True)

########################################################################
