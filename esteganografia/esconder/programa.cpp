#include <iostream>
#include "esconder.h"

using namespace std;
int main(int argc, char* argv[]){
	Esconder * esconder = new Esconder();
	string mensagem = argv[1];
	string arquivo = argv[2];
	esconder->inserirMensagem(mensagem, arquivo);
	delete(esconder);
	return 0;
}	
