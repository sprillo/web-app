## Vectorizar test set

def vectorize_statement2(statement,dictionary):
	n = len(dictionary)
	res = [0] * n
	for word in statement:
		lo = 0
		hi = n
		while lo < hi - 1: # hi se pasa, lo no
			mid = (lo + hi)/2
			if word < dictionary[mid]:
				hi = mid
			else:
				lo = mid
		if dictionary[lo] == word:
			res[lo] = 1
	return res

def vectorize_statement(statement,dictionary):
	n = len(dictionary)
	res = [0] * n
	for word in statement[2:]:
		lo = 0
		hi = n
		while lo < hi - 1: # hi se pasa, lo no
			mid = (lo + hi)/2
			if word < dictionary[mid]:
				hi = mid
			else:
				lo = mid
		if dictionary[lo] == word:
			res[lo] = 1
	return statement[0:2] + res

		
def vectorize_statements(statements_stemmed, dictionary):
	print("Vectorizing statements ...")
	return map(lambda x: vectorize_statement(x,dictionary), statements_stemmed)