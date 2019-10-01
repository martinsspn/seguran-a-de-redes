#include <iostream>
#include "extrair.h"

using namespace std;
int main(int agrc, char * argv[]){
	Extrair * extrair = new Extrair();
	string arq = argv[1];
	cout << extrair->extrairMensagem(arq) << endl;
}


