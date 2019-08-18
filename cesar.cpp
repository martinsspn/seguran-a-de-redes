#include <iostream>
#include <fstream>
#include <string>

using namespace std;
int main(int agrc, char* argv[]){
        string auxiliar, chave, alfabeto;
	alfabeto = argv[2];
        chave = "Chave ";
        char aux;
	int j=0;
	int k=0;
        fstream fs;
        fstream mensagem;
        fs.open(argv[1], fstream::in | fstream::out | fstream::app);
        if(!fs.is_open()){
                cout << "Arquivo não abriu com sucesso!!! " << endl;
                cout << "fechando arquivo";
                return -1;
        }
        while(getline(fs, auxiliar)){
        	for(int i=0; i<alfabeto.size();i++){
			j=0;
			k=0;
			chave += to_string(i) + ".txt";
               		mensagem.open(chave, fstream::in | fstream::out | fstream::app);
                	if(!mensagem.is_open()){
				cout << "Arquivo não incializado" << endl;
			}
			while(j< auxiliar.size()){
				if (auxiliar[j] == alfabeto[k]){
					mensagem << alfabeto[(k-i + alfabeto.size()) % alfabeto.size()];
					k=-1;
					j++;
				}
				if(k == alfabeto.size()){
					j++;
					k=-1;
				}
				k++;
			}
			mensagem.close();
			chave = "Chave ";
		}
	}
	fs.close();
}
