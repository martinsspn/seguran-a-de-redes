#include <iostream>
#include <fstream>

using namespace std;
int main(int argc, char * argv[]){
	fstream e;
	fstream s;
	e.open(argv[1], fstream::in);
	s.open("mensagem.txt", fstream::out);
	string auxiliar;
	string chave;
	chave = argv[2];
	char aux;
	
	while(getline(e, auxiliar)){
		for(int i=0, j=0; i<auxiliar.size(); i++, j++){
			if(auxiliar[i] == ' '){
				s << " ";
				j--;
				continue;
			}
			aux = ((auxiliar[i]-97) - (chave[j%chave.size()]-97) + 26) % 26;
			aux += 97;
			s << aux;
		}
		s << endl;
	}
	e.close();
	s.close();	
}
