import os
import sys
import shutil
import hashlib
import getopt
import hmac

def filesList(pasta): #Função para adicionar todos os arquivos da pasta em uma lista
    files = []
    for r, d, f in os.walk(pasta):
        for file in f:
            if str(os.path.join(r, file)) == str(diretorio+'/.guarda.txt'):
                continue
            elif str(os.path.join(r, file)) == str(diretorio+'/.listaGuarda.txt'):
                continue
            elif str(os.path.join(r, file)) == str(diretorio+'/guarda.py'):
                continue
            elif str(os.path.join(r, file)) == str(diretorio+'/'+saida): 
                continue
            files.append(os.path.join(r, file))
    return files #Retorna a lista com as funções

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


if saida != '': #caso a opção -o for executada abrirá um arquivo para imprimir a saida do programa
    arq_saida = open(saida, 'a')
if opcao == 0: #opção = 0 -> executando a opção -i
    verificacao = open('.listaGuarda.txt', 'a+') #verifica numa lista que estará na mesma pasta que o programa guarda se a pasta já está sendo monitorada
    verificacao.seek(0)
    os.chdir(pasta) #pegando o caminho completo da pasta
    diretorio = os.getcwd()
    for linha in verificacao: #verificacao se já está sendo monitorado
        if diretorio+"\n" == linha:
            if saida == '':
                print ("Pasta já está sendo monitorada")
            else:
                arq_saida.write("Pasta já está sendo monitorada\n")
            sys.exit()
    guarda = open(diretorio+'/.guarda.txt', 'w') #cria um arquivo txt numa pasta dentro da pasta monitorada onde esse txt guarda os hash's dos arquivos da pasta monitorada
    if metodo == 0: #se estiver sendo executado a opção --hash imprimira no arquivo oculto o valor correspondente ao metodo hash (0)
        guarda.write(str(metodo)+"\n")
    else: #se estiver sendo executado a opção --hmac imprimira no arquivo oculto o valor correspondente ao metodo (1) e a senha usada para encriptação
        guarda.write(str(metodo)+senha+"\n")
    verificacao.write(diretorio+"\n") #escreve no arquivo de verificacao a nova pasta que está sendo monitorada
    verificacao.close() 
    files = filesList(diretorio) #usando a função filesList para salvar a lista de arquivos dentro da pasta passada no programa 
    hashes = [] #criando uma lista contendo os hash's dos arquivos que estão nas pastas
    for f in files: #gerando o hash de cada arquivo e colocando na lista de hash's
        if metodo == 0: #metodo = 0 -> metodo sendo utilizado para gerar o hash é o --hash
            hasher = hashlib.md5() # ---iniciando geração de hash sem criptografia
            hasher.update(open(f, 'rb').read())
            hashes.append(hasher)  # ---finalizando geração de hash sem criptografia
        elif metodo == 1: #metodo = 1 -> metodo sendo utilizado para gerar o hash é o --hmac
            hasher = hmac.new(senha.encode("utf-8")) # ---iniciando geração de hash com criptografia
            hasher.update(open(f,'rb').read())
            hashes.append(hasher) #---finalizando geração de hash com criptografia
    for i in range(len(hashes)): #para cada arquivo na pasta
        arquivo = files[i]
        guarda.write("/" + arquivo[1:] + " > " + hashes[i].hexdigest() + "\n") #escreve no arquivo dentro da pasta monitorada os hash's dos arquivos
    guarda.close()
    if saida == '': #se -o não for executado imprime na tela
        print ("A pasta está sendo monitorada!!!")
    else: #se -o está sendo executado imprime no arquivo de saida
        arq_saida.write("A pasta está sendo monitorada!!!\n")

elif opcao == 1: #opção = 1 -> executando a opção -t
    verificacao = open('.listaGuarda.txt', 'r') #abre arquivo de verificação das pastas que estão sendo monitoradas
    verificacao.seek(0)
    os.chdir(pasta) #pegando caminho completo da pasta
    diretorio = os.getcwd()
    tracking = False #logica para definir se a pasta está sendo monitorada ou não
    for linha in verificacao: #se a pasta for igual ao caminho que está gravado dentro do arquivo de verificacao a variável tracking recebe True 
        if diretorio+"\n" == linha:
            tracking = True
    if tracking == True: #se tracking é verdade então a pasta está sendo monitorada pelo guarda
        guarda = open(diretorio+'/.guarda.txt', 'r')
        metodo = guarda.readline() #salvando metadados do arquivo .guarda
        files = filesList(diretorio) #---------------iniciando geração de hash dos arquivos da pasta
        hashes = []
        if metodo[0] == '0':
            for f in files:
                hasher = hashlib.md5()
                hasher.update(open(f, 'rb').read())
                hashes.append(hasher)
        else:
            senha = metodo[1:len(metodo)-1]
            for f in files:
                hasher = hmac.new(senha.encode("utf-8"))
                hasher.update(open(f,'rb').read())
                hashes.append(hasher) #--------------finalizando geração de hash dos arquivos da pasta
        dicionario = {} #criando um dicionario para adicionar os arquivos junto com seus respectivos hash's
        for i in range(len(hashes)):
            dicionario[str(files[i])] = hashes[i].hexdigest() #preenchendo dicionario
        arquivos = dicionario.keys() #criando uma lista que guarda as chaves do dicionario
        for linha in guarda: #logica para verificação dos arquivos
            if dicionario.get(linha[:len(linha[:len(linha)-36])]) != None:
                if dicionario.get(linha[:len(linha[:len(linha)-36])]) != linha[len(linha)-33:len(linha)-1]: #se o arquivo está na lista e no dicionario mas
                    if saida == '': #o arquivo está diferente, então o arquivo foi alterado
                        print ("O arquivo " + linha[:len(linha[:len(linha)-36])] + " foi alterado !!!")
                    else:
                        arq_saida.write("O arquivo " + linha[:len(linha[:len(linha)-36])] + " foi alterado !!!\n")
            else: #se o arquivo está na lista mas não está no dicionario então o arquivo foi removido
                if saida == '':
                    print("O arquivo " + linha[:len(linha[:len(linha)-36])] + " foi removido !!!")
                else:
                    arq_saida.write("O arquivo " + linha[:len(linha[:len(linha)-36])] + " foi removido !!!\n")
        for i in arquivos:
            novoArquivo = True #logica adicional para verificar se foi adicionado um novo arquivo
            guarda.seek(0)
            guarda.readline()
            for linha in guarda:
                if i == linha[:len(linha[:len(linha)-36])]:
                    novoArquivo = False
            if novoArquivo == True: #se o arquivo estiver no dicionario mas não estiver na lista então esse arquivo foi adicionado
                if saida == '': #logo, quando um novo arquivo não estiver na lista novo arquivo vai ser True e entrara no if acima
                    print ("O arquivo " + i + " foi adicionado!!!")#imprime na tela
                else:
                    arq_saida.write("O arquivo " + i + " foi adicionado!!!\n")#imprime no arquivo de saida

    else: #se o tracking for falso então a pasta não está sendo monitorada
        if saida == '': 
            print("Diretorio não está sendo monitorada pelo guarda!!!")
        else:
            arq_saida.write("Diretorio não está sendo monitorada pelo guarda!!!\n")
        sys.exit()

elif opcao == 2: #opcao = 2 -> executando a opcao -x 
    if pasta == "all": #se o parametro do -x for a palavra 'all' então o guarda desabilitara a guarda para todas as pastas
        verificacao = open('.listaGuarda.txt', 'r') #abre a lista que contem as pastas selecionadas
        for linha in verificacao: #apagando os arquivos ocultos de cada pasta que está sendo monitorada
            os.remove(linha[:len(linha)-1]+'/.guarda.txt') 
        verificacao.close()
        os.remove('.listaGuarda.txt')#por fim apaga o arquivo de lista de pastas pois a lista estará vazia já que nenhuma pasta está sendo monitorada
        if saida == '':
            print ("Desabilitando monitoramento para todas as pastas monitoradas!!!")
        else:
            arq_saida.write("Monitoramento desligado para todas as pastas!!!\n")
    else: #desabilita o tracking apenas para a pasta que está sendo passada por parametro do -x
        os.chdir(pasta) #pegando caminho completo da pasta
        apagar = os.getcwd()+'/.guarda.txt'
        os.remove(apagar) #removendo o arquivo oculto da pasta informada
        verificacao = open('.listaGuarda.txt', 'r')
        auxiliar = open('.auxiliar.txt', 'w')
        for linha in verificacao: #cria um arquivo auxiliar para apagar a informação de tracking na lista de tracking do programa
            if linha[:len(linha)-1]+'/.guarda.txt' == apagar:
                continue
            auxiliar.write(linha)
        verificacao.close()
        auxiliar.close()
        os.remove('.listaGuarda.txt') #apaga a lista de monitoramento que tem a pasta que foi desabiltada
        os.rename('.auxiliar.txt', '.listaGuarda.txt') #renomeia o arquivo auxiliar para o nome original da lista de monitoramento, agora sem a pasta desabilitada
        if saida == '':
            print("Monitoramento para a pasta foi desabilitado!!!")
        else:
            arq_saida.write("Monitoramento para a pasta foi desabilitado!!!\n")

if saida != '':
    arq_saida.close() #fechando o arquivo de saida
