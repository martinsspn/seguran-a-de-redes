import os
import sys
import shutil
import hashlib
import getopt
import hmac

def filesList(pasta):
    files = []
    for r, d, f in os.walk(pasta):
        for file in f:
            if str(os.path.join(r, file)) == str(diretorio+'/.guarda.txt'):
                continue
            elif str(os.path.join(r, file)) == str(diretorio+'/.listaGuarda.txt'):
                continue
            elif str(os.path.join(r, file)) == str(diretorio+'/guarda.py'):
                continue
            files.append(os.path.join(r, file))
    return files

argv = sys.argv[1:]

saida = ''
try:
    opts, args = getopt.getopt(argv, "i:t:x:o:", ["hash", "hmac="]) #usando o get opt para pegar as informações do terminal
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
        pasta = arg
    elif opt == '-o':
        saida = arg
    elif opt == '--hash':
        metodo = 0
    elif opt == '--hmac':
        metodo = 1
        senha = arg

if opcao == 0: #opção = 0 -> executando a opção -i
    verificacao = open('.listaGuarda.txt', 'a+') #verifica numa lista que estará na mesma pasta que o programa guarda se a pasta já está sendo monitorada
    verificacao.seek(0)
    os.chdir(pasta)
    diretorio = os.getcwd()
    print(diretorio)
    for linha in verificacao:
        if diretorio+"\n" == linha:
            print ("Pasta já está sendo monitorada")
            sys.exit()
    guarda = open(diretorio+'/.guarda.txt', 'w') #cria um arquivo txt numa pasta dentro da pasta monitorada onde esse txt guarda os hash's dos arquivos da pasta monitorada
    guarda.write(str(metodo)+"\n")
    verificacao.write(diretorio+"\n") #escreve no arquivo de verificacao a nova pasta que está sendo monitorada
    verificacao.close()
    files = filesList(diretorio) 
    hashes = []
    for f in files:
        if metodo == 0: #metodo = 0 -> metodo sendo utilizado para gerar o hash é o --hash
            hasher = hashlib.md5()
            hasher.update(open(f, 'rb').read())
            hashes.append(hasher)
        elif metodo == 1: #metodo = 1 -> metodo sendo utilizado para gerar o hash é o --hmac
            hasher = hmac.new(senha.encode("utf-8"))
            hasher.update(open(f,'rb').read())
            hashes.append(hasher)
    for i in range(len(hashes)):
        arquivo = files[i]
        guarda.write("/" + arquivo[1:] + " > " + hashes[i].hexdigest() + "\n") #escreve no arquivo dentro da pasta monitorada os hash's dos arquivos
    guarda.close()
    print ("A pasta está sendo monitorada!!!")

elif opcao == 1:
    verificacao = open('.listaGuarda.txt', 'a+')
    verificacao.seek(0)
    os.chdir(pasta)
    diretorio = os.getcwd()
    tracking = False
    for linha in verificacao:
        if diretorio+"\n" == linha:
            tracking = True
    if tracking == True:
        guarda = open(diretorio+'/.guarda.txt', 'r')
        metodo = guarda.readline()
        files = filesList(diretorio)
        hashes = []
        if metodo[0] == '0':
            for f in files:
                hasher = hashlib.md5()
                hasher.update(open(f, 'rb').read())
                hashes.append(hasher)
        else:
            for f in files:
                hasher = hmac.new(senha.encode("utf-8"))
                hasher.update(open(f,'rb').read())
                hashes.append(hasher)
        dicionario = {}
        for i in range(len(hashes)):
            dicionario[str(files[i])] = hashes[i].hexdigest()
        arquivos = dicionario.keys()
        #for i in arquivos:
        for linha in guarda:
            if dicionario.get(linha[:len(linha[:len(linha)-36])]) != None:
                if dicionario.get(linha[:len(linha[:len(linha)-36])]) != linha[len(linha)-33:len(linha)-1]:
                    print ("O arquivo " + linha[:len(linha[:len(linha)-36])] + " foi alterado !!!")
            else:
                #print(str(dicionario.get(linha[:len(linha[:len(linha)-36])])) +">>"+ linha[len(linha)-36:len(linha)-1])
                #print(linha[len(linha)- 33:len(linha)-1] + 'AAA')
                print("O arquivo " + linha[:len(linha[:len(linha)-36])] + " foi removido !!!")
        guarda.seek(2)
        for i in arquivos:
            novoArquivo = True
            for linha in guarda:
                if i == linha[:len(linha[:len(linha)-36])]:
                    novoArquivo = False
                    break
            if novoArquivo == True:
                print ("O arquivo " + i + " foi adicionado!!!")
    else:
        print("Diretorio não está sendo monitorada pelo guarda!!!")
        sys.exit()

elif opcao == 2: #opcao = 2 -> executando a opcao -x 
    if pasta == "all":
        verificacao = open('.listaGuarda.txt', 'r') #abre a lista que contem as pastas selecionadas
        for linha in verificacao: 
            os.remove(linha[:len(linha)-1]+'/.guarda.txt')
        verificacao.close()
        os.remove('.listaGuarda.txt')#por fim apaga o arquivo de lista de pastas pois a lista estará vazia já que nenhuma pasta está sendo monitorada
        if saida == '':
            print ("Desabilitando monitoramento para todas as pastas monitoradas!!!")
        else:
            arq_saida = open(saida, 'a+')
            arq_saida.write("Monitoramento desligado para todas as pastas!!!\n")
            arq_saida.close()
    else:
        os.chdir(pasta)
        apagar = os.getcwd()+'/.guarda.txt'
        os.remove(apagar)
        verificacao = open('.listaGuarda.txt', 'r')
        auxiliar = open('.auxiliar.txt', 'w')
        for linha in verificacao:
            if linha[:len(linha)-1]+'/.guarda.txt' == apagar:
                continue
            auxiliar.write(linha)
        verificacao.close()
        auxiliar.close()
        os.remove('.listaGuarda.txt')
        os.rename('.auxiliar.txt', '.listaGuarda.txt')
        if saida == '':
            print("Monitoramento para a pasta foi desabilitado!!!")
        else:
            arq_saida = open(saida, 'a+')
            arq_saida.write("Monitoramento para a pasta foi desabilitado!!!")
