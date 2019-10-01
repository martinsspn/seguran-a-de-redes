class SDESE:
	import sys

	def bini(self,i):
		aux = [0,0,0,0,0,0,0,0]
		byte = bin(ord(i));
		r = 0
		for j in range(9-len(byte),9):
			if r == 0 or r == 1:
				pass
			else:
				aux[j-1]=int(byte[r]);
			r = r+1	
		return aux
	def perm_IP(self,aux):
		IP = [2,6,3,1,4,8,5,7]
		perm1 = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
			perm1[j] = aux[IP[j]-1]
		return perm1
	def perm_IPi(self,aux):
		IPi =[4,1,3,5,7,2,8,6]
		perm1 = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
			perm1[j] = aux[IPi[j]-1]
		return perm1
	def perm_EP(self,perm1):
		EP = [3,0,1,2,1,2,3,0]
		perm2 = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
			perm2[j] = perm1[EP[j]+4]
		return perm2
	def function(self,perm2,perm1,key):
		lista = [0,0,0,0,0,0,0,0]
		ultima = [0,0,0,0,0,0,0,0]
		mid = [0,0,0,0]
		l = [0,0,0,0]
		P4 = [2,4,3,1]
		S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
		S1 = [[1,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
		atual = self.xor(key,perm2,lista)
		linha1 = self.transbd(atual[0],atual[3])
		coluna1 = self.transbd(atual[1],atual[2])
		valor1 = self.transdb(S0[linha1][coluna1])
		linha2 = self.transbd(atual[4],atual[7])
		coluna2 = self.transbd(atual[5],atual[6])
		valor2 = self.transdb(S1[linha2][coluna2])
		valor = valor1+valor2
		for j in range(0,4):
			mid[j] = int(valor[P4[j]-1]) 
		valor = self.xor(mid,perm1[:4],l)
		for j in range(0,4):
			ultima[j] = valor[j]
		for j in range(4,8):
			ultima[j] = perm1[j]
		return ultima
	def switch(self,ultima):
		final = [0,0,0,0,0,0,0,0]
		for j in range(0,4):
			final[j] = ultima[j+4]
		for j in range(4,8):  
			final[j] = ultima[j-4]
		return final
	def transbd(self,v1,v2):
		if(v1 == 0 and v2 == 0):
			return 0
		if(v1 == 0 and v2 == 1):
			return 1
		if(v1 == 1 and v2 == 0):
			return 2
		if(v1 == 1 and v2 == 1):
			return 3
	def transdb(self,v1):
		if v1 == 0:
			return '00'
		if v1 == 1:
			return '01'
		if v1 == 2:
			return '10'
		if v1 == 3:
			return '11'
	def xor(self,n1,n2,lista):
		for x in range(0,len(lista)):
			if (n1[x] == n2[x]):
				lista[x] = 0
			else:
				lista[x] = 1
		return lista


	def gerarChaves(self,n,chave):
		listaP10 = [3,5,2,7,4,10,1,9,8,6];
		listaP8 = [6,3,7,4,8,5,10,9];
		key = [0,0,0,0,0,0,0,0,0,0]
		final = [0,0,0,0,0,0,0,0]

		for i in range(0,10):
			key[i] = chave[listaP10[i]-1];

		for i in range(0,5):
			if (i == 0):
				aux = key[0];
			if (i == 4):
				key[4] = aux;
			else:
				key[i] = key[i+1];
			
		for i in range(5,10):
			if (i == 5):
				aux = key[5];
			if (i == 9):
				key[9] = aux;
			else:
				key[i] = key[i+1];
			
		if (n == 2):
			for i in range(0,2):
				for i in range(0,5):
					if (i == 0):
						aux = key[0];
					if (i == 4):
						key[4] = aux;
					else:
						key[i] = key[i+1];
			
				for i in range(5,10):
					if (i == 5):
						aux = key[5];
					if (i == 9):
						key[9] = aux;
					else:
						key[i] = key[i+1];

		for i in range(0,8):
			final[i] = int(key[listaP8[i]-1]);
		return final;

	def complet(self,string,key):
		
		key1 = self.gerarChaves(1,key)
		key2 = self.gerarChaves(2,key)
		s = ''
		for x in string:

			aux = self.bini(x)
			perm1 = self.perm_IP(aux)

			perm2 = self.perm_EP(perm1)	
			meio = self.function(perm2,perm1,key1)
			prox = self.switch(meio)

			perm3 = self.perm_EP(prox)
			fim = self.function(perm3,prox,key2)

			letra = self.perm_IPi(fim)
			a =''
			for x in letra:
				a += str(x)
			b = int(a,2)

			s += chr(b)
		return s
class SDESD:
	import sys

	def bini(self,i):
		aux = [0,0,0,0,0,0,0,0]
		byte = bin(ord(i));
		r = 0
		for j in range(9-len(byte),9):
			if r == 0 or r == 1:
				pass
			else:
				aux[j-1]=int(byte[r]);
			r = r+1	
		return aux
	def perm_IP(self,aux):
		IP = [2,6,3,1,4,8,5,7]
		perm1 = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
			perm1[j] = aux[IP[j]-1]
		return perm1
	def perm_IPi(self,aux):
		IPi =[4,1,3,5,7,2,8,6]
		perm1 = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
			perm1[j] = aux[IPi[j]-1]
		return perm1
	def perm_EP(self,perm1):
		EP = [3,0,1,2,1,2,3,0]
		perm2 = [0,0,0,0,0,0,0,0]
		for j in range(0,8):
			perm2[j] = perm1[EP[j]+4]
		return perm2
	def function(self,perm2,perm1,key):
		lista = [0,0,0,0,0,0,0,0]
		ultima = [0,0,0,0,0,0,0,0]
		mid = [0,0,0,0]
		l = [0,0,0,0]
		P4 = [2,4,3,1]
		S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
		S1 = [[1,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
		atual = self.xor(key,perm2,lista)
		linha1 = self.transbd(atual[0],atual[3])
		coluna1 = self.transbd(atual[1],atual[2])
		valor1 = self.transdb(S0[linha1][coluna1])
		linha2 = self.transbd(atual[4],atual[7])
		coluna2 = self.transbd(atual[5],atual[6])
		valor2 = self.transdb(S1[linha2][coluna2])
		valor = valor1+valor2
		for j in range(0,4):
			mid[j] = int(valor[P4[j]-1]) 
		valor = self.xor(mid,perm1[:4],l)
		for j in range(0,4):
			ultima[j] = valor[j]
		for j in range(4,8):
			ultima[j] = perm1[j]
		return ultima
	def switch(self,ultima):
		final = [0,0,0,0,0,0,0,0]
		for j in range(0,4):
			final[j] = ultima[j+4]
		for j in range(4,8):  
			final[j] = ultima[j-4]
		return final
	def transbd(self,v1,v2):
		if(v1 == 0 and v2 == 0):
			return 0
		if(v1 == 0 and v2 == 1):
			return 1
		if(v1 == 1 and v2 == 0):
			return 2
		if(v1 == 1 and v2 == 1):
			return 3
	def transdb(self,v1):
		if v1 == 0:
			return '00'
		if v1 == 1:
			return '01'
		if v1 == 2:
			return '10'
		if v1 == 3:
			return '11'
	def xor(self,n1,n2,lista):
		for x in range(0,len(lista)):
			if (n1[x] == n2[x]):
				lista[x] = 0
			else:
				lista[x] = 1
		return lista


	def gerarChaves(self,n,chave):
		listaP10 = [3,5,2,7,4,10,1,9,8,6];
		listaP8 = [6,3,7,4,8,5,10,9];
		key = [0,0,0,0,0,0,0,0,0,0]
		final = [0,0,0,0,0,0,0,0]
                for i in range(0,10):
			key[i] = chave[listaP10[i]-1];

		for i in range(0,5):
			if (i == 0):
				aux = key[0];
			if (i == 4):
				key[4] = aux;
			else:
				key[i] = key[i+1];
			
		for i in range(5,10):
			if (i == 5):
				aux = key[5];
			if (i == 9):
				key[9] = aux;
			else:
				key[i] = key[i+1];
			
		if (n == 2):
			for i in range(0,2):
				for i in range(0,5):
					if (i == 0):
						aux = key[0];
					if (i == 4):
						key[4] = aux;
					else:
						key[i] = key[i+1];
			
				for i in range(5,10):
					if (i == 5):
						aux = key[5];
					if (i == 9):
						key[9] = aux;
					else:
						key[i] = key[i+1];

		for i in range(0,8):
			final[i] = int(key[listaP8[i]-1]);
		return final;

	def complet(self,string,key):
		
		key1 = self.gerarChaves(1,key)
		key2 = self.gerarChaves(2,key)
		s = ''
		for x in string:

			aux = self.bini(x)
			perm1 = self.perm_IP(aux)

			perm2 = self.perm_EP(perm1)	
			meio = self.function(perm2,perm1,key2)
			prox = self.switch(meio)

			perm3 = self.perm_EP(prox)
			fim = self.function(perm3,prox,key1)

			letra = self.perm_IPi(fim)
			a =''
			for x in letra:
				a += str(x)
			b = int(a,2)

			s += chr(b)
		return s
