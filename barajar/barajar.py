import random

virg = ','
recuo = {
	'\t':	4,
    ' ': 1
}

def contarecuo (p, r = 0, valores = recuo):
	
	try:
		if type(p) != str:
			return p.recuo

		for c in p:
			r += valores[c]
	except AttributeError:
		return contarecuo(p[0],r,valores)
	except KeyError:
		pass
	return r

	
def linhas (prog):
	if type(prog) == str:
		prog = prog.splitlines()
	c = len(prog)
	prox = None
	while c > 0:
		c += -1
		prox = linha(prog[c],prox)
		prog[c] = prox
	return prog


class linha:

	def seguinte (self, next = None):
		
		try:
			if next == None:	
				return self.prox
		#	else:
			self.indentar = next.recuo - self.recuo
		except AttributeError:
			pass
		else:
			pass

		self.prox = next

	def linha (self, ln = None, ind = recuo):

		if ln == None:
			try:
				return self.ln
			except AttributeError:
				pass

		self.recuo = c = 0
		self.cru = ln
		try:
			while c < len(ln):
				self.recuo += ind[ln[c]]
				c += 1
		except KeyError:
			pass
		except TypeError:
			self.ln = ln
			return
		self.ln = ln[c:]

	def __str__ (self):
		return self.cru.__str__()
	
	def __repr__ (self, link = False):
		s = virg + ' '
		if link and self.prox != None:
			s += self.prox.__repr__(link - 1) + virg
		else:
			s += 'identation = '
		return self.__class__.__name__ + '(' + self.ln.__repr__() + s + '%d)'%self.recuo

	def __init__ (self, valor = None, prox = None, indentation = recuo):
		self.seguinte(prox)
		self.linha(valor, indentation)
	#	self.cont = cont

def embaralhar (*programas):
	programas = list(programas) # lista de listas (estas últimas que podem ser encadeadas) que serão utilizadas
	embaralhado = [] # programa de resultado

	while len(programas) > 0:
		s = random.randint(0,len(programas)-1)
		s = programas.pop(s)
		try:
			if type(s) == list:
				embaralhado.append(s.pop(0))
			else:
				embaralhado.append(s)
				s = s.prox
		except AttributeError:
			pass # caso a linha não tenha uma próxima, 
		else:	 # ela não é mantida no rol de sorteio
			if len(s):
				programas.append(s)
	return embaralhado



print(linhas(open('barajar/barajar/barajar.py','r',encoding='utf8').read()))
print(embaralhar([0,2,4,6,8],[1,[3,5,7],9,11,13,15,16],-1))