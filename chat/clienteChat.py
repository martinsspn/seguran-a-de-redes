# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from rc4 import *
from sdes import *
from diffiehellman import *
import random
import time
random.seed(time.time())

if len(sys.argv) != 5:
        print "Correct usage: script, IP address, nickname, 'q', 'alpha'"
        exit()

sdese = SDESE()
sdesd = SDESD()
rc4 = RC4()
chavePrivada = random.randint(0, int(sys.argv[3])-1)
q = sys.argv[3]
a = sys.argv[4]
obj = DiffieHellman(int(q), int(a), chavePrivada)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
IP_address = str(sys.argv[1]) 
Port = 5354 
server.connect((IP_address, Port)) 
nickname = sys.argv[2]
x = 2
chavePublica = obj.getPublicKey()
chave = ""
enviarChave = 0
receberChave = 0
abriu = 1
end = 0
isNick = 0
en = 1
foieu = 0
while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	""" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
	if en == 1:
		server.send("*!*@" + nickname + " entrou no chat")
		en = 0
	for socks in read_sockets: 
		if socks == server: 
                    message = socks.recv(2048)
                    if message[:4] == "*!*@":
                    	print message[4:]
                    elif message == "\userlist":
                    	server.send(nickname)
                    elif isNick == 1:
       					print message
       					isNick = 0
                    elif message == "\crypt sdes":
                        x = 0
                        receberChave = 1
                        server.send(str(chavePublica))
                        print "A criptografia foi mudada para o modelo SDES"
                    elif message == "\crypt rc4":
                        x = 1
                        receberChave = 1
                        server.send(str(chavePublica))
                        print "A criptografia foi mudada para o modelo RC4"
                    elif message == "\crypt none":
                        x = 2
                        print "A Criptografia foi desabilitada"
                    elif receberChave == 1:
                        chave = obj.getChave(int(message))
                        receberChave = 0
                        if foieu == 1:
                        	server.send(str(chavePublica))
                    elif x == 0:
                        print(sdesd.complet(message, chave))
                    elif x == 1:
                        rc4.setMensagem(message)
                        print(rc4.enc_dec(chave))
                    else:
                  		print(message)
		else:
                    if enviarChave == 1:
                        server.send(str(chavePublica))
                        enviarChave = 0
                        continue
                    if en == 1:
                    	server.send("*!*@" + nickname + " entrou no chat")
                    	en = 0
                    	break
                    message = sys.stdin.readline()
                    if abriu == 1:
                        message == "\crypt sdes"
                        abriu = 0
                    if(message[:len(message)-1] == "\crypt sdes"):
                        foieu = 1
                        server.send(message[:len(message)-1])
                        receberChave = 1
                        x = 0
                        print "A criptografia foi mudada para o modelo SDES"
                    elif message[:len(message)-1] ==  "\crypt rc4":
                        x = 1
                        foieu = 1
                        server.send(message[:len(message)-1])
                        receberChave = 1
                        print "A criptografia foi mudada para o modelo RC4"
                    elif message[:len(message)-1] == "\end":
                        print "Saindo do chat..."
                        end = 1
                        break
                    elif message[:len(message)-1] == "\crypt none":
                        print "Criptografia desabilitada"
                        server.send(message[:len(message)-1])
                        x = 2
                    elif message[:len(message)-1] == "\getpublickey":
                        print "Chave publica: " + str(chavePublica)
                    elif message[:len(message)-1] == "\getsessionkey":
                        print "Chave de sessao: " + chave
                    elif message[:len(message)-1] == "\info":
                    	if x == 0:
                    		print "Criptografia atual: SDES"
                    		print "Chave(IMPORTANTE: essa chave deve ser mantida em sigilo!!!): " + chave
                    	elif x == 1:
                    		print "Criptografia atual: RC4"
                    		print "Chave(IMPORTANTE: essa chave deve ser mantida em sigilo!!!): " + chave
                    	else:
                    		print "Criptografia atual: desabilitada"
                    	print "conectador ao servidor: IP -> " + IP_address + " porta -> " + str(Port)
                    	print "Diffie Hellman: Valor de 'q' -> " + str(q) + " Valor de 'alpha' -> " + str(a)
                    elif message[:len(message)-1] == "\changeparameters":
                    	q = int(input("Digite o novo valor de 'q'(OBS: o valor de 'q' so mudara no seu cliente, certifique-se de usar os mesmos parametros com outros clientes): "))
                    	a = int(input("Digite o novo valor de 'a'(OBS: o valor de 'a' so mudara no seu cliente, certifique-se de usar os mesmos parametros com outros clientes): "))
                    	obj.setQ(q)
                    	obj.setA(a)
                    	obj.setXA(random.randint(0, q-1))
                    	chavePublica = obj.getPublicKey() 
                    elif message[:len(message)-1] == "\commands":
                        print "---------------------------------------------------------------------------------------------------------------------------"
                        print "Lista de comandos: "
                        print "\crypt sdes --> muda a criptografia atual para sdes com uma chave gerada por Diffie Hellman com os parametros escolhidos"
                        print "\crypt rc4 --> muda a criptografia atual para rc4 com uma chave gerada por Diffie Hellman com os parametros escolhidos"
                        print "\crypt none --> desabilita a criptografia"
                        print "\getpublickey --> imprime a chave publica gerada pelo Diffie Hellman"
                        print "\getsessionkey --> imprime a chave de sessao(IMPORTANTE: essa chave deve ser mantida em sigilo!!!)"
                        print "\changeparameters --> muda os valores dos parametros do Diffie Hellman"
                        print "\userlist --> mostra todos os usuarios conectados"
                        print "\info --> mostra as informacoes do programa(Criptografia atual e informacoes do servidor)"
                        print "\end --> finaliza a conexao e fecha o programa"
                        print "---------------------------------------------------------------------------------------------------------------------------"
                    elif message[:len(message)-1] == "\userlist":
                    	isNick = 1
                    	server.send(message[:len(message)-1])
                    	print "Lista de usuarios: "
                    else:
                        sys.stdout.write("<You> ")
                        sys.stdout.write(message)
                        sys.stdout.flush()
                        message = "<" + nickname + "> " + message[:len(message)-1]
                        if x == 0:
                            server.send(sdese.complet(message, chave))
                        elif x == 1:
                            rc4.setMensagem(message)
                            server.send(rc4.enc_dec(chave))
                        else:
                            server.send(message)
	if end == 1:
		server.send("*!*@" + nickname + " saiu do chat")
		break
server.close()