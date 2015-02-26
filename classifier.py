import re

def read_weights():
	weights_file = open("weights.txt","r")
	weights_string = weights_file.read()
	sp = weights_string.split()
	nx4 = len(sp)
	assert nx4 % 4 == 0
	n = nx4 / 4
	weights = [[0] * n for i in range(4)]
	for i in range(n):
		for j in range(4):
			weights[j][i] = float(sp[4 * i + j])
	return weights
	
import tokenizer
import stemmer
import vectorizer

def read_dictionary():
	dictionary_file = open("dictionary.txt","r")
	dictionary = []
	for line in dictionary_file:
		dictionary.append(re.sub('\n','',line))
	dictionary_file.close()
	return dictionary

def read_statement():
	statement_file = open("statement.txt","r")
	statement = statement_file.read()
	statement_file.close()
	return statement

def inner_product(u, v):
	return sum(map(lambda i: u[i] * v[i], range(len(u))))

import math

def classify(statement, weights):
	probabilities = map(lambda i: 1. / (1 + math.exp(-inner_product(weights[i],statement))), range(4))
	problem_class = ["Algebra","Combinatorics","Geometry","Number Theory"]


	normalized_probabilities = map(lambda p: p / sum(probabilities), probabilities)
	assert abs(sum(normalized_probabilities) - 1.) < .001


	by_probs = map(lambda i: (normalized_probabilities[i],problem_class[i]), range(4))
	by_probs = sorted(by_probs)[::-1]

	res = map(lambda i:"Problem belongs to " + by_probs[i][1] + " with probability " + str(int(100 * by_probs[i][0])) + " %", range(4))

	return res


weights = read_weights()
dictionary = read_dictionary()

def classify_statement(statement):
	statement = tokenizer.tokenize_statement(statement)
	statement = stemmer.stem_statement2(statement)
	statement = vectorizer.vectorize_statement2(statement,dictionary)
	statement = [1] + statement
	return classify(statement,weights)

