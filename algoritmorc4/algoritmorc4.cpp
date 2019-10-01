#include <iostream>
#include <fstream>
#include <algorithm>

using namespace std;

int main(int argc, char* argv[]){
	fstream e;
	fstream s;
	e.open(argv[1], fstream::in);
	s.open("cifrado.txt", fstream::out);
	unsigned char S[256];
	unsigned char T[256];
	string K = argv[2];
	string mensagem;
	string aux;
    	while(getline(e, aux)){
        	mensagem += aux;
    	}
	if(K.size() > 256){
		cout << "chave de critografia muito grande" << endl;
		cout << "tente outra chave e tente novamente" << endl;
		return -1;
	}
	for(unsigned int i=0; i<256; i++){
		S[i] = i;
		T[i] = K[i % K.size()];
	}
	 int j=0;
        for(unsigned int i=0; i<256;i++){
            j = (j + S[i] + K[i % K.size()]) % 256;
            swap(S[i], S[j]);
        }
        unsigned int i=0, t=0;
	unsigned char k;
	char aux1;
        for(int y=0; y < mensagem.size(); y++){
            i = (i+1) % 256;
            j = (j + S[i]) % 256;
            swap(S[i], S[j]);
            t = (S[i] + S[j]) % 256;
            k = S[t];
	    aux1 = k ^ mensagem[y];
	    s << aux1;
	}
	s << endl;

}
		
