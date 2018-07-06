#-*- coding: UTF-8 -*-

"""
INSTITUTO FEDERAL SUL-RIO-GRANDENSE 
CURSO TÉCNICO EM INFORMÁTICA
REDES DE COMPUTADORES
PROF: MARCUS SILVA

SAPUCAIA DO SUL-RS, JUNHO DE 2018.

DESCRIÇÃO: 

Exemplo de servidor multithread com socket TCP.
O servidor é iniciado com endereço de localhost e porta especificada (12001).
Cada nova conxão estabelecida inicia uma nova thread que aguarda o envio de mensagens.
Várias mensagens podem ser recebidas após o registro da conexão. 
A receber uma msg com o comando "SAIR", a referida conexão deve ser finalizada.

"""


#Bibliotecas
from socket import *
import thread
import hashlib
from cript import Cript

porta = 12002
host = ''
enc = Cript()


def create_connection ():

	clienteSoc = socket(AF_INET, SOCK_STREAM)
	clienteSoc.connect((host, porta))
	
	print "Conexão estabelecida com sucesso!\n"
	
	return clienteSoc

def register_user ():
	while True:

		nick = raw_input( 'Informe o seu nome de usuario: ')

		clienteSoc.send(make_hash(nick))
		msg = clienteSoc.recv(1024)

		if msg == "{} conectado com sucesso.\n".format(nick):
			print "Seu usuário foi cadastrado com sucesso"
			break
		else:
			print "{}".format(msg)	

def make_hash(text):
	crypt = enc.encrypt(text)
	return bytearray(hashlib.sha224(crypt).hexdigest() + "HASH" + crypt, "utf-8")
	
def socket_send (clienteSoc):
	print "\nEscolha o comando: \n-FIM\n-LIST = Lista os usuários conectados\n-MSG = Para enviar uma  msg.\n"
	aux = raw_input('')
	if aux is not '':
		if aux == 'FIM':
			print "Tchau!\n"
			clienteSoc.send(make_hash('SAIR'))
			thread.exit()
			clienteSoc.close()
			exit(1)
		else:
			comando = aux.split()[0]
			if comando == 'LIST' or comando == 'MSG_TO':
				if comando == 'LIST':
					clienteSoc.send(make_hash(comando))
				if comando == 'MSG_TO':
					clienteSoc.send(make_hash(aux))

def socket_receive (clienteSoc):
	while True:
		msg = clienteSoc.recv(1024)
		if msg is not "":
			print msg

if __name__ == '__main__':

	try:
		clienteSoc = create_connection()
		register_user()
		thread.start_new_thread(socket_receive, (clienteSoc, ))
		while True:
			socket_send(clienteSoc)
	except timeout:
  		print "Tempo exedido!"
	except error:
  		print "Erro no Cliente:", host
  		exit(1)

