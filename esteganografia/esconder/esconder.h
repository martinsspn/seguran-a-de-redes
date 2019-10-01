#ifndef ESCONDER_H
#define ESCONDER_H
 
#include <string>
#include <iostream>
#include <cstdlib>
#include <cstdio>
using namespace std;
 
struct RGB{
    char verde;
    char vermelho;
    char azul;
};
 
struct CabecalhoBitmap{
    char identificador[2];
    int tamanho; 
    short int areaReservada1; 
    short int areaReservada2;
    int enderecoInicial; 
};
 
struct CabecalhoMapaBits{
    int tamanho;
    int largura;
    int altura; 
    short int planosCor;
    short int bpp; 
    int metodoCompressao; 
    int tamanhoImagem; 
    int resolucaoHorizontal; 
    int resolucaoVertical; 
    int coresNaPaleta; 
    int coresImportantes;
};
 
class Esconder{
private:
    FILE *arquivo;
    FILE *mensagem;
    CabecalhoBitmap cabecalho;
    CabecalhoMapaBits cabDados;
    string nomeArquivo;
    char bytesDeAjuste; 
    void esconderMensagem(string mensagem);
    void salvarBitmap();
public:
    RGB *pixels;
    int qtdePixels;
    Esconder();
    ~Esconder();
    void inserirMensagem(string mensagem, string arquivo);
};
 
#endif
