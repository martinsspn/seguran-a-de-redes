#ifndef EXTRAIR_H
#define EXTRAIR_H

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

class Extrair{
private:
    FILE *arquivo;
    FILE *mensagem;
    CabecalhoBitmap cabecalho;
    CabecalhoMapaBits cabDados;
    string nomeArquivo;
    char bytesDeAjuste; 
    string extrairMensagem();

public:
    RGB *pixels;
    int qtdePixels;
    Extrair();
    ~Extrair();
    string extrairMensagem(string arquivo);
};

#endif // EXTRAIR_H

