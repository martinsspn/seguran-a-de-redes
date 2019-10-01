class RC4:
    def _init_(self):
        self.result = ""

    def setMensagem(self, mens):
        self.mensagem = mens;
    
    def enc_dec(self, chave):
        self.result = "";
        S = []
        T = []
        K = []
        if(len(chave) > 256):
            return "chave muito grande"
        for i in chave:
            K.append(i);

        for i in range(256):
            S.append(i);
            
        j = 0
        for i in range(256):
            j = (j + S[i] + ord(K[i%len(chave)])) % 256;
            S[i], S[j] = S[j], S[i];
        i=0b0;
        t=0b0;
    
        for char in self.mensagem:
            i = (i+1) % 256;
            j = (j + S[i]) % 256;
            S[i], S[j] = S[j], S[i];
            t = (S[i] + S[j]) % 256;
            k = S[t];
            aux = chr(k ^ ord(char));
            self.result += aux;
        return self.result

