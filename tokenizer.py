import re

# TESTEAR ''TODAS'' LAS REGEX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def tokenize_statement(statement):

	features_extra = ''
	
	statement = re.sub('\\\\\\\\','\\\\',statement)
	statement = re.sub('&lt;','<',statement)
	statement = re.sub('&gt;','>',statement)
	
	# saco los caracteres molestos
	# los pesos y llaves los saco al final porque me sirven para identificar cosas de geometria con certeza
	statement = re.sub('\\\\bigl\(','(',statement)
	statement = re.sub('\\\\bigr\)',')',statement)
	statement = re.sub('\\\\left\(','(',statement)
	statement = re.sub('\\\\right\)',')',statement)
	
	statement = re.sub('co-prime','coprime',statement)
	statement = re.sub('positive[ ]+integers?',' __POSITIVEINTEGERS ',statement)
	statement = re.sub('(non-?)?[ ]*negative[ ]+integers?',' __NONNEGATIVEINTEGERS ',statement)
	statement = re.sub('positive[ ]+reals?[ ]+(numbers?)?',' __POSITIVEREALNUMBERS ',statement)
	statement = re.sub('(non-?)?[ ]*negative[ ]+reals?[ ]+(numbers?)?',' __NONNEGATIVEREALNUMBERS ',statement)
	statement = re.sub('pairwise[ ]+neighbour(ing)?',' __PAIRWISENEIGHBOURING ',statement)
	statement = re.sub('relatively([ ]+(co)?(prime))?',' __RELATIVELYPRIME ',statement)
	statement = re.sub('perfect[ ]+squares?',' __PERFECTSQUARES ',statement)
	statement = re.sub('perfect[ ]+cubes?',' __PERFECTCUBES ',statement)
	statement = re.sub('perfect[ ]+powers?',' __PERFECTPOWERS ',statement)
	statement = re.sub('inte(ger|gral)[ ]+sides?[ ]*(lengths?)?',' __INTEGERSIDELENGTH ',statement)
	
	statement = re.sub('\\\\pmod',' __LATEXPMOD ',statement)
	statement = re.sub('\\\\equiv',' __LATEXEQUIV ',statement)
	statement = re.sub('\\\\sqrt',' __LATEXSQRT ',statement)
	statement = re.sub('\^\{\\\\circ\}',' __LATEXPOWCIRC ',statement)
	statement = re.sub('\\\\d?frac',' __LATEXFRACT ',statement)
	statement = re.sub('\\\\prod(_\{[^\}]*\}\^\{[^\}]*\})?',' __LATEXPRODUCT ',statement)
	statement = re.sub('\\\\sum(_\{[^\}]*\}\^\{[^\}]*\})?',' __LATEXSUM ',statement)
	
	# $ 2014! $
	#statement = re.sub('\$[^\$]+![^\$]+\$',' __LATEXFACTORIAL ',statement)
	if re.search('\$[^\$]+![^\$]+\$',statement,0):
		features_extra = features_extra + ' __LATEXFACTORIAL '
	
	
	
	################## DECLARACION DE FUNCIONES #########################
	# TIENE QUE VENIR ANTES QUE EXPONENCIACION
	
	# $f : \mathbb Z \rightarrow \mathbb N_{\ge 0}$
	statement = re.sub('[a-z,A-Z]+[ ]*:[^\$]*\{?(Z|N)\}?((\^|_)?((\+)|(\{[^\}]\})))?[ ]*\\\\((rightarrow)|(to))[^\$]*\{?(Z|N)\}?((\^|_)?((\+)|(\{[^\}]\})))?',' __LATEXINTEGRALFUNCIONDEFINITION ',statement)
	
	# $f : \mathbb R \rightarrow \mathbb R_{\ge 0}$
	statement = re.sub('[a-z,A-Z]+[ ]*:[^\$]*\{?R\}?((\^|_)?((\+)|(\{[^\}]\})))?[ ]*\\\\((rightarrow)|(to))[^\$]*\{?R\}?((\^|_)?((\+)|(\{[^\}]\})))?',' __LATEXREALFUNCIONDEFINITION ',statement)
		
	# $f : \mathbb Z \rightarrow \mathbb N_{\ge 0}$
	statement = re.sub('[a-z,A-Z]+[ ]*:[^\$]*\{?(Z|N|Q)\}?((\^|_)?((\+)|(\{[^\}]\})))?[ ]*\\\\((rightarrow)|(to))[^\$]*\{?(Z|N|Q)\}?((\^|_)?((\+)|(\{[^\}]\})))?',' __LATEXRATIONALFUNCIONDEFINITION ',statement)
	
	# $f : \mathbb R \rightarrow \mathbb N_{\ge 0}$
	statement = re.sub('[a-z,A-Z]+[ ]*:[^\$]*\{?(R|Z|N|Q)\}?((\^|_)?((\+)|(\{[^\}]\})))?[ ]*\\\\((rightarrow)|(to))[^\$]*\{?(R|Z|N|Q)\}?((\^|_)?((\+)|(\{[^\}]\})))?',' __LATEXGENERALFUNCIONDEFINITION ',statement)
	
	
	################## DECLARACION DE TIPOS #########################
	# TIENE QUE VENIR DESPUES DE DECLARACION DE FUNCIONES Y ANTES QUE EXPONENCIACION
	
	# y\\in\\mathbb{Z_{\\ge 0}}
	statement = re.sub('[a-z,A-Z][ ]*\\\\in[ ]*[^\$]*\{?Z(\^|_)((\+)|(\{[^\}]*\}))\}?',' __LATEXVARINZSOMETHING ',statement)
	
	# \\mathbb Z^{\\ge 0}
	statement = re.sub('\\\\mathbb[ ]*\{?Z(\^|_)((\+)|(\{[^\}]*\}))\}?',' __LATEXZSOMETHING ',statement)
	
	# y\\in\\mathbb{Z}
	statement = re.sub('[a-z,A-Z][ ]*\\\\in[ ]*[^\$]*\{?Z\}?',' __LATEXVARINZ ',statement)
	
	# \\mathbb Z
	statement = re.sub('\\\\mathbb[ ]*\{?Z\}?',' __LATEXZ ',statement)
	
	
	# y\\in\\mathbb{R_{\\ge 0}}
	statement = re.sub('[a-z,A-Z][ ]*\\\\in[ ]*[^\$]*\{?R(\^|_)((\+)|(\{[^\}]*\}))\}?',' __LATEXVARINRSOMETHING ',statement)
	
	# \\mathbb R^{\\ge 0}
	statement = re.sub('\\\\mathbb[ ]*\{?R(\^|_)((\+)|(\{[^\}]*\}))\}?',' __LATEXRSOMETHING ',statement)
	
	# y\\in\\mathbb{R}
	statement = re.sub('[a-z,A-Z][ ]*\\\\in[ ]*[^\$]*\{?R\}?',' __LATEXVARINR ',statement)
	
	# \\mathbb R
	statement = re.sub('\\\\mathbb[ ]*\{?R\}?',' __LATEXR ',statement)
		
	
	# y\\in\\mathbb{Q_{\\ge 0}}
	statement = re.sub('[a-z,A-Z][ ]*\\\\in[ ]*[^\$]*\{?Q(\^|_)((\+)|(\{[^\}]*\}))\}?',' __LATEXVARINQSOMETHING ',statement)
	
	# \\mathbb Q^{\\ge 0}
	statement = re.sub('\\\\mathbb[ ]*\{?Q(\^|_)((\+)|(\{[^\}]*\}))\}?',' __LATEXQSOMETHING ',statement)
	
	# y\\in\\mathbb{Q}
	statement = re.sub('[a-z,A-Z][ ]*\\\\in[ ]*[^\$]*\{?Q\}?',' __LATEXVARINQ ',statement)
	
	# \\mathbb Q
	statement = re.sub('\\\\mathbb[ ]*\{?Q\}?',' __LATEXQ ',statement)
	
	
	########################## EXPONENCIACION ###########################
	
	# ^2 OJO QUE LOS \{? \}? MATCHEAN COSAS COMO x^{2t}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#statement = re.sub('\^(2)',' __LATEXEXPTWO ',statement)
	if re.search('\^(2)',statement,0):
		features_extra = features_extra + ' __LATEXEXPTWO '
		statement = re.sub('\^(2)',' ',statement)
	
	#statement = re.sub('\^(\{2\})',' __LATEXEXPTWO ',statement)
	if re.search('\^(\{2\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPTWO '
		statement = re.sub('\^(\{2\})',' ',statement)
	
	# ^3
	#statement = re.sub('\^(\d)',' __LATEXEXPGETHREE ',statement)
	if re.search('\^(\d)',statement,0):
		features_extra = features_extra + ' __LATEXEXPGETHREE '
		statement = re.sub('\^(\d)',' ',statement)
		
	#statement = re.sub('\^(\{\d+\})',' __LATEXEXPGETHREE ',statement)
	if re.search('\^(\{\d+\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPGETHREE '
		statement = re.sub('\^(\{\d+\})',' ',statement)
	
	# ^m
	#statement = re.sub('\^((m|n))',' __LATEXEXPMorN ',statement)
	if re.search('\^((m|n))',statement,0):
		features_extra = features_extra + ' __LATEXEXPMorN '
		statement = re.sub('\^((m|n))',' ',statement)

	#statement = re.sub('\^(\{(m|n)\})',' __LATEXEXPMorN ',statement)
	if re.search('\^(\{(m|n)\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPMorN '
		statement = re.sub('\^(\{(m|n)\})',' ',statement)
	
	# ^p
	#statement = re.sub('\^(p)',' __LATEXEXPP ',statement)
	if re.search('\^(p)',statement,0):
		features_extra = features_extra + ' __LATEXEXPP '
		statement = re.sub('\^(p)',' ',statement)
	
	#statement = re.sub('\^(\{p\})',' __LATEXEXPP ',statement)
	if re.search('\^(\{p\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPP '
		statement = re.sub('\^(\{p\})',' ',statement)
	
	# ^r
	#statement = re.sub('\^((q|r))',' __LATEXEXPQ ',statement)
	if re.search('\^((q|r))',statement,0):
		features_extra = features_extra + ' __LATEXEXPQ '
		statement = re.sub('\^((q|r))',' ',statement)
	
	#statement = re.sub('\^(\{(q|r)\})',' __LATEXEXPQ ',statement)
	if re.search('\^(\{(q|r)\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPQ '
		statement = re.sub('\^(\{(q|r)\})',' ',statement)
	
	# ^z
	#statement = re.sub('\^((x|y|z))',' __LATEXEXPXorYorZ ',statement)
	if re.search('\^((x|y|z))',statement,0):
		features_extra = features_extra + ' __LATEXEXPXorYorZ '
		statement = re.sub('\^((x|y|z))',' ',statement)

	#statement = re.sub('\^(\{(x|y|z)\})',' __LATEXEXPXorYorZ ',statement)
	if re.search('\^(\{(x|y|z)\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPXorYorZ '
		statement = re.sub('\^(\{(x|y|z)\})',' ',statement)
	
	# ^s
	#statement = re.sub('\^([a-z,A-Z])',' __LATEXEXPSTRANGELETTER ',statement)
	if re.search('\^([a-z,A-Z])',statement,0):
		features_extra = features_extra + ' __LATEXEXPSTRANGELETTER '
		statement = re.sub('\^([a-z,A-Z])',' ',statement)
	
	#statement = re.sub('\^(\{[a-z,A-Z]\})',' __LATEXEXPSTRANGELETTER ',statement)
	if re.search('\^(\{[a-z,A-Z]\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPSTRANGELETTER '
		statement = re.sub('\^(\{[a-z,A-Z]\})',' ',statement)
	
	# ^{a_n}
	#statement = re.sub('\^(\{[^\}]\})',' __LATEXEXPOTHER ',statement)
	if re.search('\^(\{[^\}]*\})',statement,0):
		features_extra = features_extra + ' __LATEXEXPOTHER '
		#statement = re.sub('\^(\{[^\}]*\})',' ',statement)
	# los ^ que queden... No deberian quedar mas, o si?
	statement = re.sub('\^',' ',statement)
	
	
	
	
	
	# h(x)
	statement = re.sub('[f,g,h]\((x|y|z)\)',' __LATEXFUNCTIONOFXYZ ',statement)
	
	# h(m)
	statement = re.sub('[f,g,h]\((n|m)\)',' __LATEXFUNCTIONOFNM ',statement)
	
	# h(1)
	statement = re.sub('[f,g,h]\(0|1\)',' __LATEXFUNCTIONONZEROORONE ',statement)
	
	# 0.5
	statement = re.sub('\d+\.\d+',' __FLOAT ',statement)
	
	# 1
	statement = re.sub('\d+',' __INTEGER ',statement)
	
	# d_7
	statement = re.sub('\{?d\}?_\{?([ ]*((__INTEGER)|([a-z,A-Z]))[ ]*)\}?',' __LATEXPROBABLYDIVISOR ',statement)
	
	# R(z)
	statement = re.sub('[P,Q,R]\((x|y|z)\)',' __LATEXPOLYNOMIALOFXYZ ',statement)
	
	# R(m)
	statement = re.sub('[P,Q,R]\((n|m)\)',' __LATEXPOLYNOMIALOFNM ',statement)
	
	# R(x + y^2) # se puede mejorar para que tenga alcance maximo/minimo/(correcto :P) etc
	statement = re.sub('[P,Q,R]\([^\)]+\)',' __LATEXPOLYNOMIALGENERIC ',statement)
	
	# g(n)
	statement = re.sub('[f,g,h]\([ ]*__INTEGER[ ]*\)',' __LATEXFUNCTIONONINTEGER ',statement)
	
	# g(x + y)
	statement = re.sub('[f,g,h]\([^\)]+\)',' __LATEXFUNCTIONGENERIC ',statement)
	
	# b_m // b_5
	statement = re.sub('\{?[a-z,A-Z]\}?_\{[^\}]*\}',' __LATEXSEQUENCEELEMENT ',statement)
	statement = re.sub('\{?[a-z,A-Z]\}?_\{?([ ]*((__INTEGER)|([a-z,A-Z]))[ ]*)\}?',' __LATEXSEQUENCEELEMENT ',statement)
	
	# m \ge 3 # Tiene que venir despues de __INTEGER y antes de \\\\ge y de n m
	statement = re.sub('(n|m)[ ]*((\\\\ge)|(\<)|(\<=)|(=\<))[ ]*__INTEGER',' __MorNLEQBOUND ',statement)
	
	# m \le 3 # Tiene que venir despues de __INTEGER y antes de \\\\ge y de n m
	statement = re.sub('(n|m)[ ]*((\\\\le)|(\>)|(\>=)|(=\>))[ ]*__INTEGER',' __MorNGEQBOUND ',statement)
	
	statement = re.sub('\{(n|m)\}',' __LATEXINTEGERVAR ',statement)
	statement = re.sub('\{(x|y|z)\}',' __LATEXNONSPECIFICVAR ',statement)
	
	statement = re.sub('\$[A-Z][A-Z][A-Z][A-Z][A-Z]\$',' __LATEXPOLYGON ',statement)
	statement = re.sub('\$[A-Z][A-Z][A-Z][A-Z]\$',' __LATEXQUADRILATERAL ',statement)
	statement = re.sub('\\\\angle[ ]*[A-Z][A-Z][A-Z]',' __LATEXANGLE ',statement)
	statement = re.sub('\$[A-Z][A-Z][A-Z]\$',' __LATEXTRIANGLE ',statement)
	statement = re.sub('\$[A-Z][A-Z]\$',' __LATEXSEGMENT ',statement)
	statement = re.sub('\\Gamma',' __LATEXGAMMA ',statement)
	statement = re.sub('\\omega',' __LATEXOMEGA ',statement)
	
	
	
	statement = re.sub('\\\\lfloor',' __LATEXLFLOOR ',statement)
	statement = re.sub('\\\\rfloor',' __LATEXRFLOOR ',statement)
	statement = re.sub('\\\\lceil',' __LATEXLCEIL ',statement)
	statement = re.sub('\\\\rceil',' __LATEXRCEIL ',statement)
	
	statement = re.sub('\\\\mathbb[ ]*\{?N\}?',' __LATEXNATURALS ',statement)
	
	statement = re.sub('\|\|',' __LATEXPARALELORDIVIDESEXACTLY ',statement)
	statement = re.sub('\|',' __LATEXDIVIDESORABSVAL ',statement)
	statement = re.sub('\\\\bigcup',' __LATEXUNION ',statement)
	statement = re.sub('\\\\cup',' __LATEXUNION ',statement)
	statement = re.sub('\\\\bigcap',' __LATEXINTERSECTION ',statement)
	statement = re.sub('\\\\cap',' __LATEXINTERSECTION ',statement)
	statement = re.sub('\\\\bot',' __LATEXPERPENDICULAR ',statement)
	statement = re.sub('\\\\angle',' __LATEXANGLE ',statement)
	statement = re.sub('\\\\hat',' __LATEXANGLE ',statement)
	statement = re.sub('\\\\triangle',' __LATEXTRIANGLE ',statement)
	statement = re.sub('\\\\elem',' __LATEXELEM ',statement)
	statement = re.sub('\\\\in',' __LATEXIN ',statement)
	statement = re.sub('\\\\ni',' __LATEXNI ',statement)
	statement = re.sub('\\\\times',' __LATEXTIMES ',statement)
	
	statement = re.sub('\\\\begin\{array\}\{[^\}]*\}',' __LATEXARRAY ',statement)
	
	statement = re.sub('\>',' __LATEXG ',statement)
	statement = re.sub('\<',' __LATEXL ',statement)
	statement = re.sub('=',' __LATEXEQ ',statement)
	statement = re.sub('\-',' __LATEXMINUSORDASH ',statement)
	statement = re.sub('\+',' __LATEXPLUS ',statement)
	statement = re.sub('\*',' __LATEXTIMES ',statement)
	statement = re.sub('/',' __LATEXDIV ',statement)
	statement = re.sub('\>=',' __LATEXGE ',statement)
	statement = re.sub('=\<',' __LATEXLE',statement)
	statement = re.sub('\\\\ge ',' __LATEXGE ',statement)
	statement = re.sub('\\\\le ',' __LATEXLE ',statement)
	
	statement = re.sub('\\\\t',' ',statement)
	statement = re.sub('\\\\n',' ',statement)
	statement = re.sub('\[',' ',statement)
	statement = re.sub('\]',' ',statement)
	statement = re.sub('\?',' ',statement)
	statement = re.sub('!',' ',statement)
	statement = re.sub('"',' ',statement)
	              
	statement = re.sub('\\\\rightarrow',' __LATEXRIGHTARROW ',statement)
	
	# Saco los pesos
	statement = re.sub('\$',' ',statement)
	statement = re.sub('{',' ',statement)
	statement = re.sub('}',' ',statement)

	# ahora saco todos los caracteres que quedan, slvo espacios
	
	#  @$/#.-:&*+=[]?!(){},''"><;%
	statement = re.sub('@',' ',statement)
	statement = re.sub('\$',' ',statement)
	statement = re.sub('\.',' ',statement)
	statement = re.sub('/',' ',statement)
	statement = re.sub('#',' ',statement)
	statement = re.sub('\-',' ',statement)
	statement = re.sub(':',' ',statement)
	statement = re.sub('&',' ',statement)
	statement = re.sub('\*',' ',statement)
	statement = re.sub('\+',' ',statement)
	statement = re.sub('=',' ',statement)
	statement = re.sub('\[',' ',statement)
	statement = re.sub('\]',' ',statement)
	statement = re.sub('\?',' ',statement)
	statement = re.sub('!',' ',statement)
	statement = re.sub('\(',' ',statement)
	statement = re.sub('\)',' ',statement)
	statement = re.sub('\{',' ',statement)
	statement = re.sub('\}',' ',statement)
	statement = re.sub(',',' ',statement)
	statement = re.sub('\'',' ',statement)
	statement = re.sub('"',' ',statement)
	statement = re.sub('\>',' ',statement)
	statement = re.sub('\<',' ',statement)
	statement = re.sub(';',' ',statement)
	statement = re.sub('%',' ',statement)
	statement = re.sub('\\\\',' ',statement)
	
	# appendeo los features extra, como __LATEXFACTORIAL
	statement = statement + features_extra
	
	# colapso todos los whitespaces a uno solo
	statement = re.sub('[ ]+',' ',statement)
	
	# Falta tokenize!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	statement_tokenized = statement.split()

	
	return statement_tokenized

def tokenize(statements):
	print("Tokenizing statements ...")
	res = []
	cant = 0
	for statement in statements:
		cant = cant + 1
		if cant % 100 == 0:
			print("%i statements tokenized ..." %cant)
		# if cant == 101:
			# break
		statement = statement[1:-2]
		statement = statement.split(',',2)
		statement[0] = statement[0][1:-1]
		statement[1] = statement[1][2:-1]
		statement[2] = tokenize_statement(statement[2])
		statement = statement[0:2] + statement[2]
		res.append(statement)
	return res