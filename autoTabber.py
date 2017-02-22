from math import *

class NoteFormatConverter:
	def __init__(self):
		pass
	def filename_GuitarNotes_To_ScoreNotes(self, filename):
		f = open(filename)
		content = ""
		for line in f:
			content += line
		content = content.replace('\t',' ')
		content = content.replace('\n','')
		f.close()
		guitarNotes = self.string_To_GuitarNotes(content)
		scoreNotes = [ScoreNote.fromGuitarNote(guitarNote) for guitarNote in guitarNotes]
		return scoreNotes
	def string_To_GuitarNotes(self, string):
		res = []
		stringGuitarNotes = string.rstrip().split(" ")
		for time in range(len(stringGuitarNotes)):
			stringGuitarNotesInCurrentTime = self.getstringGuitarNotes(stringGuitarNotes[time])
			notesInCurrentTime = [GuitarNote.fromString(stringNote,time) for stringNote in stringGuitarNotesInCurrentTime]
			# Sort Guitar Notes played at current time by pitch (so that all information conveyed by the input is destroyed, except for note pitch)
			for i in range(len(notesInCurrentTime)):
				for j in range(i,len(notesInCurrentTime)):
					if notesInCurrentTime[i].getPitch() > notesInCurrentTime[j].getPitch():
						notesInCurrentTime[i], notesInCurrentTime[j] = notesInCurrentTime[j], notesInCurrentTime[i]
			for note in notesInCurrentTime:
				res.append(note)
		return res
	def getstringGuitarNotes(self, string):
		res = []
		n = len(string)
		left = 0
		while left < n:
			# find end of current note
			right = left + 1
			while right + 1 < n and not(string[right + 1] in GuitarNote.allowedStrings):
				right += 1
			currentNote = string[left:right + 1]
			res.append(currentNote)
			left = right + 1
		return res

class ScoreNote:
	@classmethod
	def fromGuitarNote(cls,guitarNote):
		return cls(GuitarNote.notePitch[guitarNote.string] + guitarNote.fret, guitarNote.time)
	def __init__(self,pitch,time):
		self.pitch = pitch
		self.time = time
	def pitch(self):
		return self.pitch
	def __str__(self):
		return str(self.pitch)

class GuitarNote:
	maxFrets = 22
	allowedStrings = ('e','B','G','D','A','E')
	allowedFingers = (1,2,3,4)
	notePitch = dict()
	notePitch['E'] = 0
	notePitch['A'] = notePitch['E'] + 5
	notePitch['D'] = notePitch['A'] + 5
	notePitch['G'] = notePitch['D'] + 5
	notePitch['B'] = notePitch['G'] + 4
	notePitch['e'] = notePitch['B'] + 5
	stringLevel= dict()
	stringLevel['E'] = 6
	stringLevel['A'] = 5
	stringLevel['D'] = 4
	stringLevel['G'] = 3
	stringLevel['B'] = 2
	stringLevel['e'] = 1
	
	@classmethod
	def fromString(cls, stringToConstructFrom, time):
		assert len(stringToConstructFrom) >= 2
		string = stringToConstructFrom[0]
		fret = int(stringToConstructFrom[1:])
		assert string in cls.allowedStrings, "inexistent string: %s"%string
		#assert 0 <= fret and fret <= cls.maxFrets, "fret is out of range: %i"%fret #Downgrade this assert to allow e.g. 'E27E29E32'
		return cls(string, fret, time)
	def __init__(self, string, fret, time):
		self.string = string
		self.fret = fret
		self.time = time
	def string(self):
		return self.string
	def fret(self):
		return self.fret
	def __str__(self):
		#return str(self.string) + str(self.fret)
		return str(self.stringLevel[self.string]) + "_" + str(self.fret)
	def getPitch(self):
		return GuitarNote.notePitch[self.string] + self.fret
	def getStringLevel(self):
		return GuitarNote.stringLevel[self.string]

class State:
	def __init__(self, stringString, fret, finger, time):
		assert stringString in GuitarNote.stringLevel
		self.stringString = stringString
		self.fret = fret
		self.finger = finger
		self.time = time
		self.stringLevel = GuitarNote.stringLevel[stringString]
	def __str__(self):
		return str(GuitarNote.stringLevel[self.stringString]) + "_" + str(self.fret) + "_f" + str(self.finger) + "_t" + str(self.time)
	def indexFingerPosition(self):
		return self.fret + 1 - self.finger

def sameIndexFingerPosition(state1,state2):
	return state1.indexFingerPosition() == state2.indexFingerPosition()
	
def calculateCompatibleStates(scoreNote):
	res = []
	for string in GuitarNote.allowedStrings:
		fret = scoreNote.pitch - GuitarNote.notePitch[string]
		if 0 <= fret and fret <= GuitarNote.maxFrets:
			guitarNote = GuitarNote(string, fret, scoreNote.time)
			for finger in GuitarNote.allowedFingers:
				compatibleState = State(string, fret, finger, scoreNote.time)
				res.append(compatibleState)
	return res

def buildHiddenStatesFromFilename(filename):
	c = NoteFormatConverter()
	scoreNotes = c.filename_GuitarNotes_To_ScoreNotes(filename)
	hiddenStates = buildHiddenStatesFromScoreNotes(scoreNotes)
	return hiddenStates

def buildHiddenStatesFromScoreNotes(scoreNotes):
	hiddenStates = []
	for scoreNote in scoreNotes:
		# Determine all compatible states for this note
		compatibleStates = calculateCompatibleStates(scoreNote)
		hiddenStates.append(compatibleStates)
	return hiddenStates

def convertStringGuitarNotesToGuitarNotes(stringGuitarNotes):
	c = NoteFormatConverter()
	guitarNotes = c.string_To_GuitarNotes(stringGuitarNotes)
	return guitarNotes

def convertStringGuitarNotesToScoreNotes(stringGuitarNotes):
	guitarNotes = convertStringGuitarNotesToGuitarNotes(stringGuitarNotes)
	scoreNotes = [ScoreNote.fromGuitarNote(guitarNote) for guitarNote in guitarNotes]
	return scoreNotes

def stateScore(state):
	badness = 0
	# Using the pinky has a cost.
	if state.finger == 4:
		badness += Graph.WEIGHT_PINKY
	# Playing on higher frets has a cost
	badness += state.indexFingerPosition() * Graph.WEIGHT_INDEX_FINGER_POSITION
	return -badness

def logPrior(state):
	return stateScore(state)

def moveScore(s1,s2):
	badness = 0
	# same time => strings played bottom-up
	if s1.time == s2.time and s1.stringLevel <= s2.stringLevel:
		badness += Graph.INF
	# Changing IFP has a cost
	badness += abs(s1.indexFingerPosition() - s2.indexFingerPosition()) * Graph.WEIGHT_IFP_DELTA
	return -badness

def computeTransitionLogLikelihood(state1, state2):
	score = moveScore(state1,state2) + stateScore(state2)
	return score

class Penalties:
	def __init__(self,wPinky = 1,wIndexFingerPosition = 0.1,wIFPDelta = 2):
		self.wPinky = wPinky
		self.wIndexFingerPosition = wIndexFingerPosition
		self.wIFPDelta = wIFPDelta
		
class Graph:
	# Global parameters
	WEIGHT_PINKY = 0
	WEIGHT_INDEX_FINGER_POSITION = 0
	WEIGHT_IFP_DELTA = 0
	BEFORE = 0
	AFTER = 1
	INF = 100000000
	@classmethod
	def setPenalties(cls,penalties):
		if hasattr(penalties, 'wPinky'):
			cls.WEIGHT_PINKY = penalties.wPinky
		if hasattr(penalties, 'wIndexFingerPosition'):
			cls.WEIGHT_INDEX_FINGER_POSITION = penalties.wIndexFingerPosition
		if hasattr(penalties, 'wIFPDelta'):
			cls.WEIGHT_IFP_DELTA = penalties.wIFPDelta
	def __init__(self, hiddenStates):
		self.hiddenStates = hiddenStates
		self.resizeGraph(hiddenStates)
		for column in range(self.columns - 1):
			# Conectar los estados de esta capa con los de la siguiete
			for rowBefore in range(self.columnSizes[column]):
				for rowAfter in range(self.columnSizes[column + 1]):
					transitionLogLikelihood = computeTransitionLogLikelihood(self.hiddenStates[column][rowBefore],self.hiddenStates[column + 1][rowAfter])
					self.g[column][rowBefore][self.AFTER][rowAfter] = transitionLogLikelihood
					self.g[column + 1][rowAfter][self.BEFORE][rowBefore] = transitionLogLikelihood
	def resizeGraph(self, hiddenStates):
		self.hiddenStates = hiddenStates
		self.columns = len(hiddenStates)
		self.columnSizes = [len(hiddenStates[column]) for column in range(self.columns)]
		self.g = [None for column in range(self.columns)]
		for column in range(self.columns):
			self.g[column] = [None for columnSize in range(self.columnSizes[column])]
			for row in range(self.columnSizes[column]):
				self.g[column][row] = [None for direction in [self.BEFORE,self.AFTER]]
				for direction in [self.BEFORE,self.AFTER]:
					if 0 <= column + self.val(direction) and column + self.val(direction) < self.columns:
						self.g[column][row][direction] = [0 for neighbour in range(self.columnSizes[column + self.val(direction)])]
	def val(self, direction):
		if direction == self.BEFORE:
			return -1
		if direction == self.AFTER:
			return 1
		assert(False)
	def longestPath(self):
		self.createDPStructs()
		# Base case
		for row in range(self.columnSizes[0]):
			self.dp[0][row] = logPrior(self.hiddenStates[0][row])
		# Recursive cases
		for column in range(1,self.columns):
			for row in range(self.columnSizes[column]):
				# dp[column][row]
				for prevRow in range(self.columnSizes[column - 1]):
					newScore = self.dp[column - 1][prevRow] + self.g[column][row][self.BEFORE][prevRow]
					if newScore > self.dp[column][row]:
						self.dp[column][row] = newScore
						self.prev[column][row] = prevRow
		# Recover longest paths
		longestPath = []
		currCol = self.columns - 1
		currRow = 0
		for row in range(self.columnSizes[self.columns - 1]):
			if self.dp[self.columns - 1][row] > self.dp[self.columns - 1][currRow]:
				currRow = row
		print("Longest path has length: %f\n"%self.dp[self.columns - 1][currRow])
		longestPath.append(currRow)
		for currCol in range(self.columns - 1,0,-1):
			currRow = self.prev[currCol][currRow]
			longestPath.append(currRow)
		longestPath = longestPath[::-1]
		return longestPath
	def createDPStructs(self):
		self.dp = [None for column in range(self.columns)]
		self.prev = [None for column in range(self.columns)]
		for column in range(self.columns):
			self.dp[column] = [-self.INF for row in range(self.columnSizes[column])]
			self.prev[column] = [-1 for row in range(self.columnSizes[column])]
	def bestStates(self):
		longestPath = self.longestPath()
		assert len(longestPath) == self.columns
		res = []
		for column in range(self.columns):
			row = longestPath[column]
			state = self.hiddenStates[column][row]
			res.append(state)
		return res
		
# For local run as when written		
def getOutputString(states):
	n = max([state.time for state in states]) + 1
	tab = [[None for c in range(n)] for r in range(len(GuitarNote.allowedStrings))]
	for stateId in range(len(states)):
		state = states[stateId]
		stringLevel = state.stringLevel
		column = state.time
		tab[stringLevel - 1][column] = str(state.fret)
	outputStr = ""
	for row in range(len(GuitarNote.allowedStrings)):
		outputStr += GuitarNote.allowedStrings[row] + ":\t"
		for column in range(n):
			if tab[row][column] is not None:
				outputStr += str(tab[row][column])
			outputStr += "\t"
		outputStr += "\n"
	return outputStr

def getOutputTabHTML(states):
	n = max([state.time for state in states]) + 1
	tab = [[None for c in range(n)] for r in range(len(GuitarNote.allowedStrings))]
	for stateId in range(len(states)):
		state = states[stateId]
		stringLevel = state.stringLevel
		column = state.time
		tab[stringLevel - 1][column] = str(state.fret)
	#~ outputStr = '<table style="width:100%">'
	outputStr = '<table>'
	for row in range(len(GuitarNote.allowedStrings)):
		outputStr += '<tr>'
		outputStr += '<td>'
		outputStr += GuitarNote.allowedStrings[row] + ":"
		outputStr += '</td>'
		for column in range(n):
			outputStr += '<td></td>'
			outputStr += '<td>'
			if tab[row][column] is not None:
				outputStr += str(tab[row][column])
			else:
				outputStr += '-'
			outputStr += '</td>'
		outputStr += '</tr>'
	outputStr += '</table>'
	return outputStr

def neatPrint(states,filename = ""):
	outputStr = getOutputString(states)
	if filename != "":
		f = open(filename,'w')
		f.write(outputStr)
		f.close()
	else:
		print(outputStr)

def toMusixtex(states):
	res = "\setlength\parindent{0pt}\\begin{music}\instrumentnumber{1}\\nobarnumbers\TAB1\setlines1{6}\startpiece"
	n = max([state.time for state in states]) + 1
	tab = [[None for c in range(n)] for r in range(len(GuitarNote.allowedStrings))]
	for stateId in range(len(states)):
		state = states[stateId]
		stringLevel = state.stringLevel
		column = state.time
		tab[stringLevel - 1][column] = str(state.fret)
	for t in range(n):
		notesAtThisTime = "\\notes"
		for stringLevel in range(1,len(GuitarNote.allowedStrings) + 1):
			if tab[stringLevel - 1][t] is not None:
				notesAtThisTime += "\str{" + str(len(GuitarNote.allowedStrings) + 1 - stringLevel) + "}{" + str(tab[stringLevel - 1][t]) + "}"
		notesAtThisTime += "\en"
		res += notesAtThisTime
	res += "\endpiece\end{music}"
	return res

def getOutputFingeringHTML(states):
	n = max([state.time for state in states]) + 1
	tab = [[None for c in range(n)] for r in range(len(GuitarNote.allowedStrings))]
	for stateId in range(len(states)):
		state = states[stateId]
		stringLevel = state.stringLevel
		column = state.time
		tab[stringLevel - 1][column] = str(state.finger)
	#~ outputStr = '<table style="width:100%">'
	outputStr = '<table>'
	for row in range(len(GuitarNote.allowedStrings)):
		outputStr += '<tr>'
		outputStr += '<td>'
		outputStr += GuitarNote.allowedStrings[row] + ":"
		outputStr += '</td>'
		for column in range(n):
			outputStr += '<td></td>'
			outputStr += '<td>'
			if tab[row][column] is not None:
				outputStr += str(tab[row][column])
			else:
				outputStr += '-'
			outputStr += '</td>'
		outputStr += '</tr>'
	outputStr += '</table>'
	return outputStr

def getOutputScoreExplanationHTML(states):
	n = max([state.time for state in states]) + 1
	tab = [[None for c in range(n)] for r in range(len(GuitarNote.allowedStrings))]
	for stateId in range(len(states)):
		state = states[stateId]
		stringLevel = state.stringLevel
		column = state.time
		if stateId == 0:
			tab[stringLevel - 1][column] = logPrior(state)
		else:
			previousState = states[stateId - 1]
			tab[stringLevel - 1][column] = computeTransitionLogLikelihood(previousState,state)
	#~ outputStr = '<table style="width:100%">'
	outputStr = '<table>'
	for row in range(len(GuitarNote.allowedStrings)):
		outputStr += '<tr>'
		outputStr += '<td>'
		outputStr += GuitarNote.allowedStrings[row] + ":"
		outputStr += '</td>'
		for column in range(n):
			outputStr += '<td></td>'
			outputStr += '<td>'
			if tab[row][column] is not None:
				outputStr += str(tab[row][column])
			else:
				outputStr += '-'
			outputStr += '</td>'
		outputStr += '</tr>'
	outputStr += '</table>'
	return outputStr

def calcAccuracy(guitarNotes,states):
	assert(len(guitarNotes) == len(states))
	assert(len(guitarNotes) > 0)
	N = len(guitarNotes)
	correct = 0
	for i in range(N):
		guitarNote = guitarNotes[i]
		state = states[i]
		if guitarNote.getStringLevel() == state.stringLevel and guitarNote.fret == state.fret:
			correct += 1
	return correct * 100 / N

def autoTab(stringGuitarNotes,wPinky,wIndexFingerPosition,wIFPDelta):
	print("Processing stringGuitarNotes:\n%s"%stringGuitarNotes)
	# Destroy all input information but the pitch of the notes
	scoreNotes = convertStringGuitarNotesToScoreNotes(stringGuitarNotes)
	# Set penalties
	Graph.setPenalties(Penalties(float(wPinky),float(wIndexFingerPosition),float(wIFPDelta)))
	# Get DAG nodes
	hiddenStates = buildHiddenStatesFromScoreNotes(scoreNotes)
	# Build graph
	g = Graph(hiddenStates)
	# Perform inference
	bestStates = g.bestStates()
	# Compute number of correct notes
	guitarNotes = convertStringGuitarNotesToGuitarNotes(stringGuitarNotes)
	accuracy = calcAccuracy(guitarNotes,bestStates)
	# Format results
	tabHTML = getOutputTabHTML(bestStates)
	fingeringHTML = getOutputFingeringHTML(bestStates)
	scoreExplanationHTML = getOutputScoreExplanationHTML(bestStates)
	print(toMusixtex(bestStates))
	return ["Tab: (I got %i%% of the input tab correctly)\n"%accuracy + tabHTML,"Finger Annotations:\n" + fingeringHTML, 'Score Explanation:\n' + scoreExplanationHTML]


