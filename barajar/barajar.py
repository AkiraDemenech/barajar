import random
import warnings

virg = ','
pyignore = '#'#, '"""',"'''"
bloco = '#@bloco;','#@bloco_acabou;'
recuo = {
    None:[4,1], #	O índice de tamanhos, em ordem decrescente
	'\t':	4,
    ' ': 1,
 1: ' ',
	4: '\t',
0:pyignore	# comentários são sinalizados pelo 0
}

def recua (r = 0, valores = recuo):
#	r += contarecuo(p,r,valores)
	t = ''
	try:
		for l in valores[None]:
			t += valores[l]*(r//l)
			r %= l
	except TypeError:
		warnings.warn('Os valores para recuo devem ser iteráveis e indicar os números das strings')
	except KeyError:
		warnings.warn('Os valores para recuo devem ter índice numérico ordenado coerente.')
	return t

def contarecuo (p, r = 0, valores = recuo):
	
	try:
		if type(p) != str:
			return p.recuo

		for c in p:
			r += valores[c]
	except AttributeError:
		if p != None:
			return contarecuo(p[0],r,valores)
	except KeyError:
		pass
	return r


def blocos (prog, novo = False, id = None, abre=bloco[0],fecha=bloco[1]):
	if novo or type(prog) != list:
		prog = linhas(prog)
	novo = True
	b = c = 0
	while c < len(prog):
		try:
			if id != None:
				prog[c].__id__((c,id))
		except AttributeError:
			pass
		if abre in prog[c]:
			prog[c] = [prog[c]]
			b = c
			c += 1
			novo = False
		elif novo:
			c += 1
		else:
			if fecha in prog[c]:
				novo = True
			prog[b].append(prog.pop(c))
	#	c += novo
	return prog
			
			
			
def texto (prog, r = 0, cab='',sep='\n',ind=recuo):
	for ln in prog:
		if type(r) != list:
			r = [contarecuo(ln,r,ind)]
		if type(ln) == list:
			cab += texto(ln,r,sep=sep,ind=ind)
		else:
			cab += recua(r[0],ind) + str(ln.ln) + sep
			r[0] += ln.indentar()
	return cab
	
def linhas (prog,prox=None,id=None,ind=recuo):
	if type(prog) == str:
		prog = prog.splitlines()
	else:
		prog = list(prog)
	c = len(prog)
	while c > 0:
		c += -1
		prox = linha(prog[c],prox,ind)
		prog[c] = prox
		if id != None:
			prog[c].__id__((c,id))
	return prog


class linha:

	def linha (self, ln = None, ind = recuo):

		if ln == None:
			try:
				return self.ln
			except AttributeError:
				pass
		elif self.__class__ == ln.__class__:
			if self.id == None:
				self.id = ln.id
			if ind == recuo:
				ind = ln.ind
			ln = ln.cru

		self.recuo = c = 0
		self.cru = self.ln = ln
		self.ind = ind
		try:
			while c < len(ln):
				self.recuo += ind[ln[c]]
				c += 1
		except KeyError:
			pass
		except TypeError:
			if type(ind) == int:
				self.recuo = ind
			return
		try:
			self.ln = ln[c:]
			ln = 0
			for c in ind[0]:
				if self.find(c) == 0:
					ln = self.__len__()
					break
		except KeyError:
			pass
		except:
			warnings.warn('Ocorreu algum problema inesperado nas linhas anteriores!',RuntimeWarning)
		if self.__len__() == ln:
			self.recuo = contarecuo(self.seguinte())#self.prox.recuo
			

	def seguinte (self, next = None):
		try:
			if next == None:	
				return self.prox
		except AttributeError:
			pass
		self.prox = next
	def list (self,refresh=False):
		i = 0
		if refresh:
		#	self.lista.clear()
			prox = self
			while prox != None:
				if self.lista[i] != prox:
					self.lista.insert(i,prox)
				i += 1
				try:
					prox = prox.prox
				except AttributeError:
					break
			while i < len(self.lista):
				self.lista.pop(i)
		return self.lista
	def indentar (self, r = 0):
		try:
			return self.prox.recuo - self.recuo
		except AttributeError:
			return r

	
	def index (self,*item):
		return self.ln.index(*item)
	def find (self, *item):
		try:
			return self.index(*item)
		#	return self.ln.find(*item)
		except AttributeError:
			return -2
		except:
			return -1
	def startswith (self, prefixo, partida=0,limite=None, passo=1):
		try:
		#	if len(prefixo)>limite-partida:
		#		return
		#except TypeError:
			return self.ln.startswith(prefixo,partida,limite)
		except AttributeError:
			if limite == None:
				limite = self.__len__()
			p = partida
			while p < limite:
				try:
					i = self[p].index(prefixo)#startswith(prefixo)
					if i == 0 or i == partida:
						return True
				except AttributeError:
					pass
				except ValueError:
					pass
				p += passo
		return self.find(prefixo)==partida; 		

	def __contains__ (self, item):
		try:
			return self.ln.__contains__(item)
		except Exception:
			return 

	def __hash__ (self):
		try:
			return self.cru.__hash__()
		except TypeError:
			return self.indentar(self.recuo).__hash__()

	def __str__ (self):
		return self.cru.__str__()
	
	def __repr__ (self, link = False):
		s = virg
		if link and self.prox != None:
			s += '\n' + ' '*self.recuo + self.prox.__repr__(link - (link > 0)) + virg
		else:
			if self.id != None:
				s += ' id = ' + str(self.id) + virg
			s += 'identation='
		return self.__class__.__name__ + '(' + self.ln.__repr__() + s + '%d)'%self.recuo

	def __reversed__ (self, refresh = None):
		return self.list(refresh).__reversed__()
	def __iter__ (self, refresh = None):
		return self.list(refresh).__iter__()

	def __init__ (self, valor = None, prox = None, indentation = recuo, id = None):
		if prox == None and valor.__class__ == self.__class__:
			prox = valor.prox
		self.id = id
		self.lista = []
		self.seguinte(prox)
		self.linha(valor, indentation)
		
		

	def __id__ (self,id=None):
		if id == None:
			return self.id
		self.id = id

	def __gt__ (self,outro):
		return not self.__le__(outro)
	def __lt__ (self,outro):
		return not self.__ge__(outro)
	def __eq__ (self,outro):
		return not self.__ne__(outro)

	def __ne__ (self, outro):		
		if self.__class__ == outro.__class__:
			return self.recuo != outro.recuo or self.ln != outro.ln
		return (self.cru != outro and self.ln != outro) or outro == None
	def __ge__ (self, outro):
		try:
			return self.recuo >= outro.recuo or self.indentar() >= outro.indentar() 
		except AttributeError:	
			return self.__str__() > str(outro) or self.__eq__(outro)
	def __le__ (self, outro):	
		try: 
			return self.recuo <= outro.recuo or self.indentar() <= outro.indentar()
		except AttributeError:
			return self.__str__() < str(outro) or self.__eq__(outro)
	def __len__ (self, novo = None, partida = None, passo = None):
		try:
			if novo != None:
				if type(novo) != slice:
					novo = slice(partida,novo,passo)
				self.ln = self.ln[novo]
			return self.ln.__len__()
		except AttributeError:
			return -1

	def __getitem__ (self, i): 
		try:
			return self.ln[i]
		except IndexError:
			return self.ln
		except KeyError:
			return self
		except: 
			return 

	
		
			

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



print(linhas(open('barajar/barajar/barajar.py','r',encoding='utf8').read(),id = 0))
print(linha('    a',linha('   a',None,14),10).find('a'))
print(linha(linha('	a'),linha(' a')).find('a'))
print(embaralhar([0,2,4,6,8],[1,[3,5,7],9,11,13,15,16],-1))
for l in blocos(open('barajar/barajar/barajar.py','r',encoding='utf8').read()): 
	if len(l) == 0:
		print(l.__repr__(1))
print(linha()[0])
print(recua('       123423532').__repr__())