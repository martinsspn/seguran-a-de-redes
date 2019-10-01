#include "extrair.h"

Extrair::Extrair(){
}

Extrair::~Extrair(){
}

string Extrair::extrairMensagem(string arquivo){
    this->arquivo = fopen(arquivo.c_str(), "rb");
    if(!this->arquivo)
    {
        cout << " Arquivo nao encontrado..." << endl;
        system("pause");
        return string("");
    }

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
            continue; 
        }

        fread(&pixels[pix++], sizeof(RGB), 1, this->arquivo); 
        larg++;
    }

    fclose(this->arquivo);

    string mensagem;

    mensagem = this->extrairMensagem();

    return mensagem;
}

string Extrair::extrairMensagem(){
    string mensagem;
    char caracter;
    int indice = 0;

    do{
        caracter = (pixels[indice].vermelho & 1) +
                   ((pixels[indice].verde & 1) * 2) +
                   ((pixels[indice].azul & 1) * 4) +
                   ((pixels[indice+1].vermelho  & 1) * 8 ) +
                   ((pixels[indice+1].verde & 1) * 16) +
                   ((pixels[indice+1].azul & 1) * 32) +
                   ((pixels[indice+2].vermelho & 1) * 64) +
                   ((pixels[indice+2].verde & 1) * 128);
	
	/*caracter = ((pixels[indice].vermelho & 1) * 128) +
		   ((pixels[indice].verde & 1) * 64) +
		   ((pixels[indice].azul & 1) * 32) +
		   ((pixels[indice+1].vermelho & 1) * 16) +
		   ((pixels[indice+1].verde & 1) * 8) + 
		   ((pixels[indice+1].azul & 1) * 4) +
		   ((pixels[indice+2].vermelho & 1) * 2) +
		   (pixels[indice+2].verde & 1);
        */
	mensagem += caracter;
        indice += 3;
    }while (caracter != 3);

    mensagem = mensagem.substr(0, mensagem.length() - 1);
    return mensagem;
}

