import random
import warnings
from _io import TextIOWrapper

virg = ','
pyignore = '#'#, '"""',"'''"
bloco = '#@B','#@A'
recuo = {
    None:[4,1], #	O índice de tamanhos, em ordem decrescente
	'\t':	4,
    ' ': 1,
 1: ' ',
	4: '\t',
0:pyignore	# comentários são sinalizados pelo 0
}

def recua (r = 0, valores = recuo):
	'''Dados uma posição de tabulação inicial inteira r e o dicionário valores ordenando inteiros e caracteres de indentação, 
	 retorna uma string equivalente ao número fornecido orientado pelo índice na chave None.'''
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
	'''Retorna o recuo da linha p somada à tabulação inicial r conforme o dicionário dos valores dos caracteres,
	se p já não tiver recuo calculado.'''
	
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
	'''Divide a lista de linhas prog (sendo essa lista copiada se novo for verdadeiro),
	atribuindo, se possível, o id != None, abrindo os blocos e fechando de acordo com a presença das substrings fornecidas.
	
	O id é composto pela tupla do valor dado precedido pelo índice da lista, se o referido valor não for None.'''
	if novo or type(prog) != list:
		prog = linhas(prog)
	novo = True
	b = c = 0
	while c < len(prog):
		ln = prog[c]
		try:
			ln = ln.upper()
			if id != None:
				prog[c].__id__((c,id))
		except AttributeError:
			pass
		if abre in ln:
			prog[c] = [prog[c]]
			b = c
			c += 1
			novo = False
		elif novo:
			c += 1
		else:
			if fecha in ln:
				novo = True
			prog[b].append(prog.pop(c))
	#	c += novo
	return prog
			
			
			
def texto (prog, r = 0, cab='',sep='\n',ind=recuo):
	'''Retorna o texto da lista de linhas prog com o recuo geral inteiro r com os caracteres do dicionário ind, a string de cabeçalho cab e sep como separador de linha.'''
	for ln in prog:
		if type(r) != list:
			r = [contarecuo(ln,r,ind)]
		if type(ln) == list:
			cab += texto(ln,r,sep=sep,ind=ind)
		else:
			cab += recua(r[0],ind) + str(ln.linha()) + sep
			r[0] += ln.indentar()
	return cab
	
def linhas (prog,prox=None,id=None,ind=recuo,carrega=True):
	'''Inicializa a lista (e as referências de lista ligada) prog,
	referenciando a linha prox ao final, se id != None, atribui-o e conta o recuo inteiro pelo dicionário de indentação ind.

	O id é composto pela tupla do valor dado precedido pelo índice da lista, se o referido valor não for None.
	Ao final da função, o argumento carrega (verdadeiro por padrão) é fornecido para que a lista ligada completa seja montada (ou não) na primeira linha'''
	if type(prog) == TextIOWrapper:
		p = prog.read()
	#	prog.close()
		prog = p
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
	if len(prog) > 0:
		prog[0].list(carrega)
	return prog


class linha:

	def linha (self, ln = None, ind = recuo):
		'''Getter e setter do atributo .ln sem a indentação, calculando também o .recuo com base no dicionário de caracteres ou valor final ind, igualado ao recuo da próxima linha se esta não tiver valor significativo (for inteiramente comentada ou completamente vazia).
		Guarda o original no atributo .cru'''

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
		fonte = str(ln)
		self.recuo = c = 0
		self.cru = self.ln = ln
		self.ind = ind
		self.lower = fonte.lower
		self.upper = fonte.upper
		self.title = fonte.title
		self.split = fonte.split
		self.splitlines = fonte.splitlines
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
			

	def anterior (self, previous = None, update = True):
		'''Setter e getter do link para a linha prévia, por padrão também tenta atualizar o link dela para a seguinte (esta).
		Atenção: não há atualização do link para a seguinte aqui se isso for solicitado explicitamente, assim podendo causar distorções e discordâncias se esse método for utilizado sozinho.'''
		try:
			if previous == None:	
				return self.prev
			if update:
				previous.seguinte(self)
		except AttributeError:
			pass
		self.prev = previous
	def seguinte (self, next = None):
		'''Setter e getter do link para a próxima linha.
		Atenção: não há atualização da lista ligada completa aqui, deve-se solicitar recarregamento explicitamente.'''
		try:
			if next == None:	
				return self.prox
			next.anterior(self,False)
		except AttributeError:
			pass
		self.prox = next
	def list (self,refresh=False):
		'''Getter e updater (se bool(refresh) == True) da lista ligada finita de todas as próximas linhas.
		A lista termina no link None ou quando a segunda aparição do self for atingida
		O retorno do método .seguinte é considerado link, não mais o atributo .prox
		Se refresh for uma lista, .lista é atualizada para a nova referência'''
		i = 0
		if list == type(refresh):
			self.lista = refresh
		if refresh:
		#	self.lista.clear()
			prox = self
			while prox != None:
				if i >= len(self.lista) or self.lista[i] != prox:
					self.lista.insert(i,prox)
				i += 1
				try:
					prox = prox.seguinte()
					if self == prox:
						break
				except AttributeError:
					break
			while i < len(self.lista):
				self.lista.pop(i)
		return self.lista
	def add (self,l,refresh=None):
		'''Adiciona a linha ao final da lista (se for cíclica, considera o verdadeiro self.anterior() como o último elemento) e atualiza a lista ligada completa, se for pedido'''
		self.append(l)
		self.list(refresh)
	def append (self, l):
		'''Acrescenta a linha l ao final da lista.
		Se descobre que a lista é circular (reencontrando self), adiciona imediatamente antes dele.'''
		self.insert(True,l)
	def insert (self, i,*l):
		'''Insere as linhas l antes do índice i dado
		Os objetos de l deve ter o método .seguinte, caso algum não tenha, a continuidade da lista é cortada na sua posição
		A precisão do corte se um objeto for diferente de None não é garantida
		Caso i seja o bool True, insere depois da última linha (na lista circular é a verdadeira self.anterior())
		Não há atualização implícita da lista ligada completa'''
		seguinte = self
		anterior = self.anterior()
		while i < 0 and anterior != None:
			i += 1
			seguinte = anterior
			anterior = anterior.anterior()
		while i > 0 and seguinte != None:
			if type(i) != bool:
				i -= 1
			elif self==seguinte:
				break
			anterior = seguinte
			seguinte = seguinte.seguinte()
		for ln in l:
			try:
				if seguinte != None:	#essa redundância garante o corte da lista se ln.seguinte não existir/puder ser executado
					seguinte.anterior(ln)
				if anterior != None:
					anterior.seguinte(ln)
				ln.seguinte(seguinte)
			except AttributeError:
				pass
			except:
				warnings.warn('Ocorreu algum problema inesperado nas atribuições da sequência;')
			anterior = ln

		'''
		refresh = self.list(refresh)
		if i >= len(refresh):
			i = len(refresh)
		if i >= 0:
			if i:
				anterior = refresh[i-1]
			anterior.seguinte(l)
		self.list(refresh).insert(i,l)'''
	def indentar (self, r = 0):
		'''Calcula a diferença entre o recuo da próxima linha e o recuo da linha atual, caso não exista algum dos dois recuos, retorna o argumento r'''
		try:
			return self.prox.recuo - self.recuo
		except AttributeError:
			return r

	
	def index (self,*item):
		'''Sem tratamento de erro,
		mais informações, se houver, em self.ln.index.__doc__
		'''
		return self.ln.index(*item)
	def find (self, *item):
		'''Retorna o índice do item conforme .ln.index
		Caso seja encontrado problema, retorna -1;	
		Caso não haja .index em .ln, retorna -2;	'''
		try:
			return self.index(*item)
		#	return self.ln.find(*item)
		except AttributeError:
			return -2
		except:
			return -1
	def startswith (self, prefixo, partida=0,limite=None, passo=1):
		'''Retorna verdadeiro se o prefixo tiver índice igual à partida (0 por padrão) em .ln (caso seja string).
		Caso .ln.__class__ != str, verifica se algum elemento entre a partida e o limite (__len__, por padrão), com incremento passo (por padrão 1), possui o prefixo em índice 0 ou igual à partida. A soma do índice com o passo não é protegida de exceções.
		Caso nada seja encontrado, retorna self.find(prefixo) == partida.'''
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
		'''item in self.ln
		Excepcionalmente retorna None.
		'''
		try:
			return self.ln.__contains__(item)
		except Exception:
			return 

	def __hash__ (self):
		'''Hash da linha bruta, se .cru tiver .__hash__, 
		caso contrário, retorna a hash da variação de tabulação, se houver recuo na linha seguinte e, 
		se não tiver, utiliza a hash do recuo (inteiro).'''
		try:
			return self.cru.__hash__()
		except TypeError:
			return self.indentar(self.recuo).__hash__()

	def __str__ (self):
		'''str(self.cru)
		'''
		return self.cru.__str__()
	
	def __repr__ (self, link = False):
		'''Retorna a representação textual da linha refinada (.ln), se link != 0, inclui as link próximas linhas também (se link < 0, todas as próximas, sem tratamento de listas circulares).
		A inicialização pela representação perde o dicionário do recuo .ind original e também perde o id se for exibir a lista ligada.'''
		s = virg
		if link and self.prox != None:
			s += '\n' + ' '*self.recuo + self.prox.__repr__(link - (link > 0)) + virg
		else:
			if self.id != None:
				s += ' id = ' + str(self.id) + virg
			s += 'identation='
		return self.__class__.__name__ + '(' + self.ln.__repr__() + s + '%d)'%self.recuo

	def __reversed__ (self, refresh = None):
		'''	self.list(refresh).__reversed__()'''
		return self.list(refresh).__reversed__()
	def __iter__ (self, refresh = None):
		'''	self.list(refresh).__iter__()'''
		return self.list(refresh).__iter__()

	def __init__ (self, valor = None, prox = None, indentation = recuo, id = None):
		if prox == None:
			try:
				prox = valor.seguinte()
			except AttributeError:
				pass
		self.id = id
		self.lista = []
		self.seguinte(prox)
		self.linha(valor, indentation)
		
		

	def __id__ (self,id=None):
		'''Setter e getter do id. 
		Ele não pode ser setado para None'''
		if id == None:
			return self.id
		self.id = id

	def __gt__ (self,outro):
		'''Inversão de .__le__'''
		return not self.__le__(outro)
	def __lt__ (self,outro):
		'''Inversão de .__ge__'''
		return not self.__ge__(outro)
	def __eq__ (self,outro):
		'''Inversão de .__ne__'''
		return not self.__ne__(outro)

	def __ne__ (self, outro):		
		'''Compara o .recuo e a .ln, se o outro objeto também for uma linha, se for instância de outra classe (diferente de None), verifica se .ln ou .cru se diferenciam a ele'''
		if self.__class__ == outro.__class__:
			return self.recuo != outro.recuo or self.ln != outro.ln
		return (self.cru != outro and self.ln != outro) or outro == None
	def __ge__ (self, outro):
		'''Compara o .recuo ou a diferença de indentação se o outro objeto tiver, caso contrário, compara igualdade ou se .__str__ é maior'''
		try:
			return self.recuo >= outro.recuo or self.indentar() >= outro.indentar() 
		except AttributeError:	
			return self.__str__() > str(outro) or self.__eq__(outro)
	def __le__ (self, outro):	
		'''Compara o .recuo ou a diferença de indentação se o outro objeto tiver, caso contrário, compara igualdade ou se .__str__ é menor'''
		try: 
			return self.recuo <= outro.recuo or self.indentar() <= outro.indentar()
		except AttributeError:
			return self.__str__() < str(outro) or self.__eq__(outro)
	def __len__ (self, novo = None, partida = None, passo = None):
		'''Getter e updater do comprimento de .ln'''
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
			return
		except KeyError:
			return

	
		
			

def embaralhar (*programas):
	''' Embaralhamento simples: recebe listas para serem mescladas numa só. 
		Não observa níveis de exclusão entre itens, somente a unidade deles.

		Classes, funções, try-except e if-else não-blocados podem ter sintaxe da indentação prejudicada!'''
	programas = [list(p) for p in programas] # lista de listas (estas últimas que podem ser encadeadas) que serão utilizadas
	embaralhado = [] # programa de resultado

	while len(programas) > 0:
		s = random.randint(0,len(programas)-1)
		s = programas.pop(s)
		try:
			if type(s) == list:
				embaralhado.append(s.pop(0))
			else:
				embaralhado.append(s)
				s = s.seguinte()
		except AttributeError:
			pass # caso a linha não tenha uma próxima, 
		else:	 # ela não é mantida no rol de sorteio
			if s != None and len(s):
				programas.append(s)
	return embaralhado


if __name__ == '__main__':
	'''		
	print(linhas(open('barajar/barajar/barajar.py','r',encoding='utf8').read(),id = 0))
	print(linha('    a',linha('   a',None,14),10).find('a'))
	print(linha(linha('	a'),linha(' a')).find('a'))
	print(embaralhar([0,2,4,6,8],[1,[3,5,7],9,11,13,15,16],-1))
	for l in blocos(open('barajar/barajar/barajar.py','r',encoding='utf8').read()): 
		if len(l) == 0:
			print(l.__repr__(1))
	print(linha()[0])
	print(recua('       123423532').__repr__())
	'''
	
	tres = open('../../L-oeuvre_dada/Bingo/Bingo.java').read()
	dois = open('../../L-oeuvre_dada/Quadra/Hexa.java').read()
	um = open('../../L-oeuvre_dada//Geral.java').read()

	tres = open('../../Cobrinha/cobrinha.c').read()
	dois = open('../../Cobrinha/cobrinhas.c').read()
	um = open('../../Cobrinha//gotas.c').read()

	tres = open('..\\..\\coder_rerun\\exercises/g_bad_vibes.py').read()
	dois = open('..\\..\\coder_rerun\\exercises/c_gifts.py').read()
	um = open('..\\..\\coder_rerun\\exercises/a_cups_game.py').read()

	
	p3 = linhas(um),linhas(dois),linhas(tres)
	for p in p3:
		for l in p:
			print(l.__repr__(), l.indentar())
#	for l in p4:
#		print(l.__repr__())	
	p4 = embaralhar(*p3)
	
	quatro = open('../txt.py','w')
	quatro.write(texto(p4))
	quatro.close()

	