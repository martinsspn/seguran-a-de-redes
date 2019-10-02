import os
import sys
import shutil
import hashlib
import getopt

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "i:t:xo:", ["hash", "hmac="]) #usando o get opt para pegar as informações do terminal
except getopt.GetoptError as err:
    print(err)
    sys.exit()

for opt, arg in opts:
    if opt == '-i':
        opcao = 0
        pasta = arg
    elif opt == '-t':
        opcao = 1
        pasta = arg
    elif opt == '-x':
        opcao = 2
    elif opt == '-o':
        saida = arg
    elif opt == '--hash':
        metodo = 0
    elif opt == '--hmac':
        metodo = 1
        senha = arg

if opcao == 0: #opção = 0 -> executando a opção -i
    verificacao = open('listaGuarda.txt', 'a+') #verifica numa lista que estará na mesma pasta que o programa guarda se a pasta já está sendo monitorada
    verificacao.seek(0)
    for linha in verificacao:
        os.chdir(pasta+'./guarda')
        if os.getcwd()+"\n" == linha:
            print ("Pasta já está sendo monitorada")
            sys.exit()
    os.mkdir(pasta + './guarda')
    guarda = open(pasta+'./guarda/guarda.txt', 'w') #cria um arquivo txt numa pasta dentro da pasta monitorada onde esse txt guarda os hash's dos arquivos da pasta monitorada
    os.chdir(pasta+'./guarda')
    verificacao.write(os.getcwd()+"\n") #escreve no arquivo de verificacao a nova pasta que está sendo monitorada
    verificacao.close()
    files = []
    for r, d, f in os.walk(pasta): 
        for file in f:
            files.append(os.path.join(r, file)) 
    hashes = []
    for f in files:
        if metodo == 0: #metodo = 0 -> metodo sendo utilizado para gerar o hash é o --hash
            hasher = hashlib.md5()
            hasher.update(open(f, 'rb').read())
            hashes.append(hasher)
        elif metodo == 1: #metodo = 1 -> metodo sendo utilizado para gerar o hash é o --hmac
            hasher = hmec.new(senha.encode("utf-8"))
            hasher.update(open(f,'rb').read())

    for i in range(len(hashes)):
        guarda.write(files[i] + " > " + hashes[i].hexdigest() + "\n") #escreve no arquivo dentro da pasta monitorada os hash's dos arquivos
    guarda.close()
    print ("A pasta está sendo monitorada!!!")

elif opcao == 2: #opcao = 2 -> executando a opcao -x 
    verificacao = open('listaGuarda.txt', 'r') #abre a lista que contem as pastas selecionadas
    for linha in verificacao: # apaga recursivamente as pastas ./guarda das pastas que estão sendo monitoradas
        shutil.rmtree(linha[:len(linha)-1])
    verificacao.close()
    os.remove('listaGuarda.txt')#por fim apaga o arquivo de lista de pastas pois a lista estará vazia já que nenhuma pasta está sendo monitorada
    print ("Desabilitando monitoramento para todas as pastas monitoradas!!!")

