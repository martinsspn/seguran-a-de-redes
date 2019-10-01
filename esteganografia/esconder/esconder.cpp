#include "esconder.h"
 
Esconder::Esconder(){}
 
Esconder::~Esconder(){}
 
void Esconder::inserirMensagem(string arqmens, string arquivo){
    this->arquivo = fopen(arquivo.c_str(), "rb");
    string mensArq;
    char aux;
    if(!this->arquivo){
        cout << " Arquivo nao encontrado..." << endl;
        return;
    }
    this->mensagem = fopen(arqmens.c_str(), "r");
    if(!this->mensagem){
        cout << " Arquivo nao encontrado..." << endl;
        return;
    }
    aux = fgetc(this->mensagem);
    while(aux != EOF){
        mensArq += aux;
        aux = fgetc(this->mensagem);
    }
    aux = 3;
    mensArq += aux; 
    fclose(this->mensagem);
    nomeArquivo = arquivo;
 
    fread(&cabecalho.identificador, sizeof(cabecalho.identificador), 1, this->arquivo);
    fread(&cabecalho.tamanho, sizeof(cabecalho.tamanho), 1, this->arquivo);
    fread(&cabecalho.areaReservada1, sizeof(cabecalho.areaReservada1), 1, this->arquivo);
    fread(&cabecalho.areaReservada2, sizeof(cabecalho.areaReservada2), 1, this->arquivo);
    fread(&cabecalho.enderecoInicial, sizeof(cabecalho.enderecoInicial), 1, this->arquivo);
    fread(&cabDados.tamanho, sizeof(cabDados.tamanho), 1, this->arquivo);
    fread(&cabDados.largura, sizeof(cabDados.largura), 1, this->arquivo);
    fread(&cabDados.altura, sizeof(cabDados.altura), 1, this->arquivo);
    fread(&cabDados.planosCor, sizeof(cabDados.planosCor), 1, this->arquivo);
    fread(&cabDados.bpp, sizeof(cabDados.bpp), 1, this->arquivo);
    fread(&cabDados.metodoCompressao, sizeof(cabDados.metodoCompressao), 1, this->arquivo);
    fread(&cabDados.tamanhoImagem, sizeof(cabDados.tamanhoImagem), 1, this->arquivo);
    fread(&cabDados.resolucaoHorizontal, sizeof(cabDados.resolucaoHorizontal), 1, this->arquivo);
    fread(&cabDados.resolucaoVertical, sizeof(cabDados.resolucaoVertical), 1, this->arquivo);
    fread(&cabDados.coresNaPaleta, sizeof(cabDados.coresNaPaleta), 1, this->arquivo);
    fread(&cabDados.coresImportantes, sizeof(cabDados.coresImportantes), 1, this->arquivo);
 
    this->bytesDeAjuste = cabDados.largura % 4;
    fseek(this->arquivo, 0, SEEK_END);
    qtdePixels = cabDados.largura * cabDados.altura;
    pixels = new RGB[qtdePixels];
    fseek(this->arquivo, cabecalho.enderecoInicial, SEEK_SET);
    for (int larg = 0, pix = 0; pix < qtdePixels;){
        if (larg == cabDados.largura){
            fseek(this->arquivo, bytesDeAjuste, SEEK_CUR); 
            larg = 0;
            continue; //
        }
        fread(&pixels[pix++], sizeof(RGB), 1, this->arquivo);
        larg++;
    }
    fclose(this->arquivo);
    unsigned long capacidade = (cabecalho.tamanho - cabecalho.enderecoInicial)/3;
    if(mensArq.size() > capacidade){
        cout << "Arquivo de texto muito grande!" << endl;
        system("pause");
        return;
    }
    if(cabecalho.enderecoInicial != 0x36){
        cout << "Tipo de arquivo invalido!" << endl;
        system("pause");
        return;
    }
    this->esconderMensagem(mensArq);
    this->salvarBitmap();
    delete pixels;
};
 
void Esconder::esconderMensagem(string mensagem){
    for(unsigned int numCaracter = 0, indice = 0; numCaracter <= mensagem.size(); numCaracter++){
        this->pixels[indice].vermelho &= 254;
        this->pixels[indice].verde &= 254;
        this->pixels[indice].azul &= 254;
        this->pixels[indice].vermelho |= (mensagem[numCaracter] & 1 ? 1 : 0);
        this->pixels[indice].verde |= (mensagem[numCaracter] & 2 ? 1 : 0);
        this->pixels[indice].azul |= (mensagem[numCaracter] & 4 ? 1 : 0);
        indice++;
        this->pixels[indice].vermelho &= 254;
        this->pixels[indice].verde &= 254;
        this->pixels[indice].azul &= 254;
        this->pixels[indice].vermelho |= (mensagem[numCaracter] & 8 ? 1 : 0);
        this->pixels[indice].verde |= (mensagem[numCaracter] & 16 ? 1 : 0);
        this->pixels[indice].azul |= (mensagem[numCaracter] & 32? 1 : 0);
        indice++;
        this->pixels[indice].vermelho &= 254;
        this->pixels[indice].verde &= 254;
        this->pixels[indice].vermelho |= (mensagem[numCaracter] & 64 ? 1 : 0);
        this->pixels[indice].verde |= (mensagem[numCaracter] & 128? 1 : 0);
        indice++;
    }
};
 
void Esconder::salvarBitmap(){
    arquivo = fopen(nomeArquivo.c_str(), "wb");
    if (!arquivo){
        cout << " Impossivel criar/sobrescrever o arquivo." << endl;
        system("pause");
        exit(1);
    }
    fwrite(&cabecalho.identificador, sizeof(cabecalho.identificador), 1, arquivo);
    fwrite(&cabecalho.tamanho, sizeof(cabecalho.tamanho), 1, arquivo);
    fwrite(&cabecalho.areaReservada1, sizeof(cabecalho.areaReservada1), 1, arquivo);
    fwrite(&cabecalho.areaReservada2, sizeof(cabecalho.areaReservada2), 1, arquivo);
    fwrite(&cabecalho.enderecoInicial, sizeof(cabecalho.enderecoInicial), 1, arquivo);
 
    fwrite(&cabDados.tamanho, sizeof(cabDados.tamanho), 1, arquivo);
    fwrite(&cabDados.largura, sizeof(cabDados.largura), 1, arquivo);
    fwrite(&cabDados.altura, sizeof(cabDados.altura), 1, arquivo);
    fwrite(&cabDados.planosCor, sizeof(cabDados.planosCor), 1, arquivo);
    fwrite(&cabDados.bpp, sizeof(cabDados.bpp), 1, arquivo);
    fwrite(&cabDados.metodoCompressao, sizeof(cabDados.metodoCompressao), 1, arquivo);
    fwrite(&cabDados.tamanhoImagem, sizeof(cabDados.tamanhoImagem), 1, arquivo);
    fwrite(&cabDados.resolucaoHorizontal, sizeof(cabDados.resolucaoHorizontal), 1, arquivo);
    fwrite(&cabDados.resolucaoVertical, sizeof(cabDados.resolucaoVertical), 1, arquivo);
    fwrite(&cabDados.coresNaPaleta, sizeof(cabDados.coresNaPaleta), 1, arquivo);
    fwrite(&cabDados.coresImportantes, sizeof(cabDados.coresImportantes), 1, arquivo);
 
    char fimDeLinha[bytesDeAjuste];
    for (int i = 0; i < bytesDeAjuste; i++){
        fimDeLinha[i] = 0;
    }
    for (int pix = 0, larg = 0; pix < qtdePixels;){
        if (larg == cabDados.largura){
            fwrite(&fimDeLinha, bytesDeAjuste, 1, arquivo);
            larg = 0;
            continue;
        }
        fwrite(&pixels[pix++], sizeof(RGB), 1, arquivo);
        larg++;
    }
    fclose(arquivo);
};
