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
		stringNotes = string.rstrip().split(" ")
		for time in range(len(stringNotes)):
			stringNotesInCurrentTime = self.getStringNotes(stringNotes[time])
			for stringNote in stringNotesInCurrentTime:
				res.append(GuitarNote.fromString(stringNote,time))
		return res
	def getStringNotes(self, string):
		# need to parse this sh*t
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
		# Check notes are in order
		for i in range(len(res) - 1):
			stringNote1 = res[i][0]
			stringNote2 = res[i + 1][0]
			assert GuitarNote.stringLevel[stringNote1] > GuitarNote.stringLevel[stringNote2], "Notes played simultaneously should be provided in order"	
		return res

class ScoreNote:
	@classmethod
	def fromGuitarNote(cls,guitarNote):
		return cls(GuitarNote.noteLevel[guitarNote.string] + guitarNote.fret, guitarNote.time)
	def __init__(self,level,time):
		self.level = level
		self.time = time
	def level(self):
		return self.level
	def __str__(self):
		return str(self.level)

class GuitarNote:
	maxFrets = 21
	allowedStrings = ('e','B','G','D','A','E')
	allowedFingers = (1,2,3,4)
	noteLevel = dict()
	noteLevel['E'] = 0
	noteLevel['A'] = noteLevel['E'] + 5
	noteLevel['D'] = noteLevel['A'] + 5
	noteLevel['G'] = noteLevel['D'] + 5
	noteLevel['B'] = noteLevel['G'] + 4
	noteLevel['e'] = noteLevel['B'] + 5
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
		assert 0 <= fret and fret <= cls.maxFrets, "fret is out of range: %i"%fret
		return cls(string, fret, time)
	def __init__(self, string, fret, time):
		self.string = string
		self.fret = fret
		self.time = time
	def string(self):
		return self.string
	def getNoteLevel(self):
		return noteLevel[self.string]
	def fret(self):
		return self.fret
	def __str__(self):
		#return str(self.string) + str(self.fret)
		return str(self.stringLevel[self.string]) + "_" + str(self.fret)

class State:
	MAX_PHRASES = 2
	def __init__(self, stringString, fret, finger, phrase, time):
		self.stringString = stringString
		self.fret = fret
		self.finger = finger
		self.time = time
		assert stringString in GuitarNote.stringLevel
		self.stringLevel = GuitarNote.stringLevel[stringString]
		self.phrase = phrase
	def __str__(self):
		return str(GuitarNote.stringLevel[self.stringString]) + "_" + str(self.fret) + "_f" + str(self.finger) + "_p" + str(self.phrase) + "_t" + str(self.time)
	
def calculateCompatibleStates(scoreNote):
	res = []
	for string in GuitarNote.allowedStrings:
		for fret in range(GuitarNote.maxFrets + 1):
			guitarNote = GuitarNote(string, fret, scoreNote.time)
			if ScoreNote.fromGuitarNote(guitarNote).level == scoreNote.level:
				for finger in GuitarNote.allowedFingers:
					for phrase in range(State.MAX_PHRASES):
						compatibleState = State(string, fret, finger, phrase, scoreNote.time)
						res.append(compatibleState)
	return res

def buildGraphStatesFromFilename(filename):
	c = NoteFormatConverter()
	scoreNotes = c.filename_GuitarNotes_To_ScoreNotes(filename)
	graphStates = buildGraphStatesFromScoreNotes(scoreNotes)
	return graphStates

def buildGraphStatesFromScoreNotes(scoreNotes):
	graphStates = []
	for scoreNote in scoreNotes:
		# Determine all compatible states for this note
		compatibleStates = calculateCompatibleStates(scoreNote)
		graphStates.append(compatibleStates)
	return graphStates

def buildGraphStatesFromStringNotes(stringNotes):
	c = NoteFormatConverter()
	guitarNotes = c.string_To_GuitarNotes(stringNotes)
	scoreNotes = [ScoreNote.fromGuitarNote(guitarNote) for guitarNote in guitarNotes]
	return buildGraphStatesFromScoreNotes(scoreNotes)

def logPrior(state):
	badness = 0
	WEIGHT_INITIAL_FRET = 0
	badness += WEIGHT_INITIAL_FRET * state.fret
	WEIGHT_INITIAL_STRING = 0
	badness += WEIGHT_INITIAL_STRING * state.stringLevel
	return -badness
def computeTransitionLogLikelihood(state1, state2):
	# TODO: Open strings do not require any finger check (but should probably be penalized slightly to avoid abusing them)
	badness = 0
	# It is important to know if the notes are played at the same time
	sameTime = (state1.time == state2.time)
	############################ Same Phrase ###########################
	# Force fingers to stick to their frets
	fretOffset = state2.fret - state1.fret
	fingerOffset = state2.finger - state1.finger
	fretFingerOffset = abs(fretOffset - fingerOffset)
	#Only expection (for now): 3rd and pinky, if on same fret
	ok = False
	ok = ok or (fretFingerOffset == 0)
	ok = ok or (state1.finger == 4 and state2.finger == 3 and state1.fret == state2.fret)
	ok = ok or (state1.finger == 3 and state2.finger == 4 and state1.fret == state2.fret)
	if not ok:
		badness = Graph.INF
	if fretFingerOffset != 0:
		badness = Graph.INF
	# No string skipping beyond 1, UNLESS AT THE SAME TIME
	if (not sameTime) and abs(state1.stringLevel - state2.stringLevel) >= 3:
		badness = Graph.INF
	# Penalize string skipping slightly =======================================> I'm only using this to fix border notes between two phrases. (E.G. in Stairway to Heaven, between phrases 2 and 3)
	WEIGHT_TWO_STRING_JUMP = 0.1
	if abs(state1.stringLevel - state2.stringLevel) == 2:
		badness += WEIGHT_TWO_STRING_JUMP
	# Penalize pinky
	WEIGHT_PINKY_BADNESS = Graph.WEIGHT_PINKY_BADNESS # made 'Global'
	if state2.finger == 4:
		badness += WEIGHT_PINKY_BADNESS
	# Avoid the upper quadrant area
	WEIGHT_UPPER_QUADRANT = 2
	if state2.stringLevel >= 4 and state2.fret >= 15:
		badness += WEIGHT_UPPER_QUADRANT
	########################### New Phrase #############################
	NEW_PHRASE_BADNESS = Graph.NEW_PHRASE_BADNESS # made 'Global'
	if state2.phrase == 1 - state1.phrase:
		badness = NEW_PHRASE_BADNESS
	return -badness

class Graph:
	# Global parameters
	NEW_PHRASE_BADNESS = 10
	WEIGHT_PINKY_BADNESS = 1
	BEFORE = 0
	AFTER = 1
	INF = 100000000
	@classmethod
	def setPenalties(cls,phrasePenalty,pinkyPenalty):
		cls.NEW_PHRASE_BADNESS = phrasePenalty
		cls.WEIGHT_PINKY_BADNESS = pinkyPenalty
	def __init__(self, graphStates):
		self.graphStates = graphStates
		self.resizeGraph(graphStates)
		for column in range(self.columns - 1):
			# Conectar los estados de esta capa con los de la siguiete
			for rowBefore in range(self.columnSizes[column]):
				for rowAfter in range(self.columnSizes[column + 1]):
					transitionLogLikelihood = computeTransitionLogLikelihood(self.graphStates[column][rowBefore],self.graphStates[column + 1][rowAfter])
					self.g[column][rowBefore][self.AFTER][rowAfter] = transitionLogLikelihood
					self.g[column + 1][rowAfter][self.BEFORE][rowBefore] = transitionLogLikelihood
	def resizeGraph(self, graphStates):
		self.graphStates = graphStates
		self.columns = len(graphStates)
		self.columnSizes = [len(graphStates[column]) for column in range(self.columns)]
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
			self.dp[0][row] = logPrior(self.graphStates[0][row])
		# Recursive cases
		for column in range(1,self.columns):
			for row in range(self.columnSizes[column]):
				# dp[column][row]
				for prevRow in range(self.columnSizes[column - 1]):
					newCost = self.dp[column - 1][prevRow] + self.g[column][row][self.BEFORE][prevRow]
					if newCost > self.dp[column][row]:
						self.dp[column][row] = newCost
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
			state = self.graphStates[column][row]
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
	# Agregar '\t|' entre dos frases
	endPhrase = [False] * n
	for stateId in range(len(states) - 1):
		state1 = states[stateId]
		time = state1.time
		state2 = states[stateId + 1]
		if state1.phrase != state2.phrase:
			endPhrase[time] = True
	for column in range(n):
		if endPhrase[column]:
			for row in range(len(GuitarNote.allowedStrings)):
				if tab[row][column] is None:
					tab[row][column] = '\t|'
				else:
					tab[row][column] += '\t|'
	outputStr = ""
	for row in range(len(GuitarNote.allowedStrings)):
		outputStr += GuitarNote.allowedStrings[row] + ":\t"
		for column in range(n):
			if tab[row][column] is not None:
				outputStr += str(tab[row][column])
			outputStr += "\t"
		outputStr += "\n"
	return outputStr

def getOutputStringHTML(states):
	n = max([state.time for state in states]) + 1
	tab = [[None for c in range(n)] for r in range(len(GuitarNote.allowedStrings))]
	for stateId in range(len(states)):
		state = states[stateId]
		stringLevel = state.stringLevel
		column = state.time
		tab[stringLevel - 1][column] = str(state.fret)
	#~ # Agregar '\t|' entre dos frases
	endPhrase = [False] * n
	for stateId in range(len(states) - 1):
		state1 = states[stateId]
		time = state1.time
		state2 = states[stateId + 1]
		if state1.phrase != state2.phrase:
			endPhrase[time] = True
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
			if endPhrase[column]:
				outputStr += '<td></td>'
				outputStr += '<td>'
				outputStr += '|'
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

def autoTab(stringNotes,phrasePenalty,pinkyPenalty):
	#~ print("Processing stringNotes:\n%s"%stringNotes)
	Graph.setPenalties(int(phrasePenalty),int(pinkyPenalty))
	gs = buildGraphStatesFromStringNotes(stringNotes)
	g = Graph(gs)
	bestStates = g.bestStates()
	res = getOutputStringHTML(bestStates)
	print([str(state) for state in bestStates])
	#~ print("Returning tab:\n%s"%res)
	return [res]

# Code for local run as when written
#~ gs = buildGraphStatesFromFilename("tab.txt")
#~ g = Graph(gs)
#~ bestStates = g.bestStates()
#~ print([str(state) for state in bestStates])
#~ neatPrint(bestStates,"out.txt")
#~ neatPrint(bestStates)


