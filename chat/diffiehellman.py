class DiffieHellman:
	def __init__(self, q, a, XA):
		self.q = q
		self.a = a
		self.XA = XA
	
	def getPublicKey(self):
		Ya = self.a**self.XA % self.q
		return Ya	

	def setQ(self, q):
		self.q = q

	def setA(self, a):
		self.a = a

	def setXA(self, XA):
		self.XA = XA

	def getChave(self, Yb):
		l = ""
		k = (Yb)**self.XA % self.q
		s = bin(k)
		j=0
		
		for i in range(0,10-len(s)):
			l = l+'0'
		for i in range(0, len(s)):
			if(i == 0 or i == 1):
				l = l+'0'
			else:
				l = l+ s[i]
		if (len(l)>10):
			l = l[len(l)-10:]
		return l


