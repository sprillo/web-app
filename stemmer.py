## Stemmer

# CAREFULL! Since we are running on a server, module isn't installed.
from porter2 import stem
# package can be found here: https://pypi.python.org/pypi/stemming/1.0

def my_stem(word):
	if word == word.upper() or (len(word) >= 2 and word[0:2] == "__"):
		return word
	else:
		return stem(word.lower())

def stem_statement2(statement):
	return map(lambda x: my_stem(x),statement)

def stem_statement(statement):
	return statement[0:2] + map(lambda x: my_stem(x),statement[2:])

def stem_all(statements_tokenized):
	print("Stemming statements ...")
	return map(lambda x: stem_statement(x), statements_tokenized)