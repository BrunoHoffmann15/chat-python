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
import hashlib
import thread
import re
from cript import Cript

#Ip e Porta o servidor
porta = 12002
ip = ''	#localhost.

#Dicionário de usuários
nick_con = {} 	#Deve receber as conexões (socket) estabelecidas e a chave deve ser o nick.
enc = Cript()

#Função para estabelecer/aceitar as conexões.
def inicia_servidor(servidorSoc):
	#associa o socket a porta e ip do servidor.
	servidorSoc.bind((ip, porta)) 
	servidorSoc.listen(60)	#número de conexões simultâneas.

	print "Servidor ativo!\nAguardando conexões."

	while True:
		conexao, end_remoto = servidorSoc.accept() #chamada bloqueante
		thread.start_new_thread(trata_nova_conexao, (conexao, end_remoto))

def verify_hash(text):
	hash_mensagem = re.match(r"(.*)HASH", text).group(1)
	conteudo_msg = text.split("HASH")[1]
	hash_atual = hashlib.sha224(bytearray(conteudo_msg, "utf-8")).hexdigest()
	return hash_mensagem == hash_atual

def get_message(text):
	aux = text.decode("utf-8").split("HASH")[1].strip()
	return enc.decrypt(aux)

#Tratamento de nova conexão. 
def trata_nova_conexao(con, end_remoto):
	print "Conexao com: ", end_remoto
	nick = con.recv(1024).strip()		#Remove espaços e quebra de linhas da msg/string.
	hash_trate = verify_hash(nick)
	if hash_trate :
		nick = get_message(nick)
		if nick in nick_con.keys():			#Verifica se o usuário ja está cadastrado.
			#Envia ao cliente a mensagem de erro, usuario ja registrado, seguida da lista de todos os usuários.
			con.send(nick + " ja esta em uso.\nLista de usuarios: {}\n".format(nick_con.keys()))
			#Chamada recursiva para aguardar o novo nome de usuário.
			trata_nova_conexao(con, end_remoto)
		else:
			#Registra o novo usuário e sua conexao (socket)
			nick_con[nick] = con
			con.send(nick + " conectado com sucesso.\n")

			print nick + " conectado com sucesso.\n"

			#Loop para aguardar as mensagens.
			while True:
				msg_remota = con.recv(1024)				#Recebe as novas mensagens.
				hash_trate = verify_hash(msg_remota)
				if hash_trate :
					msg_remota = get_message(msg_remota)
					print msg_remota
					if msg_remota == '' or msg_remota == 'SAIR':	#fim da conexao com o cliente
						print "A conexao com ", nick, " foi fechada.\n"
						con.close()					#Fecha a conexão TCP
						del nick_con[nick]			#Remove o usuário da lista de regitros.
						break	

					else: 
						if msg_remota.split()[0] == "MSG_TO":
							aux = msg_remota.split("TO")[1].strip()
							user_to_send = aux.split()[0]
							msg = aux.split(user_to_send)[1].strip()
							if user_to_send in list(nick_con.keys()):	
								try:
									connection_user_to_send = nick_con[user_to_send]
									connection_user_to_send.send("MSG_FROM "+ nick+" - "+msg)
								except error:
									con.send("Ocorreu um erro")
							else:
								con.send("O usuário " + user_to_send + " não está online")				
						else:
							print "list"
							con.send("LIST_NICKS :\n{}\n".format(nick_con.keys()))	
				else:
					con.send("Sem autorizacao")				
	else:
		con.send("Sem autorizacao")

#Função principal.
if __name__ == '__main__':

	try:

		#Cria o socket TCP e inicia o servidor.
		servidorSoc = socket(AF_INET, SOCK_STREAM)	#Socket TCP
	
		#thread para iniciar o ervidor e receber novas conexões.
		thread.start_new_thread(inicia_servidor, (servidorSoc,))


		#Loop para aguadar interações com o operador. 
		#Ao digitar fim, o servidor é encerado.
		while True:
			aux = raw_input('') #leitura da entrada do usuario
			if aux == 'FIM':
				print "Tchau!\n"
				servidorSoc.close()  #nunca!
				exit(1)



	except timeout:
  		print "Tempo exedido!"
	except error:
  		print "Erro no Servidor:", host
  		exit(1)






