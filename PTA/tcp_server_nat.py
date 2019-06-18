# -*- coding: utf8 -*-
'''
README:
Executar em pyton 3.X.
Usuário válido: Vinícius.
'''

from socket import *
import os, traceback, sys

serverName = '127.0.0.1'
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")


clientes_validos, acoes = ["8610511023799105117115", "711089711799111"], ["CUMP", "LIST", "PEGA", "TERM"]

def receber_msg(cSocket):
    sentence = cSocket.recv(1024)
    sentence = sentence.decode()
    try:
        menssagem = sentence.split()
        seq_num = menssagem[0]
        comando = menssagem[1]

        if comando=="CUMP":
            args = ''.join(str(ord(c)) for c in menssagem[2])
        elif comando=="PEGA":
            args = menssagem[2]
        else:
            args = ""
    except:
        return 0, 0, 0
    return seq_num,comando,args

permissao = False

while True:
    try:
        seq_num, comando, args = receber_msg(clientSocket)

        if((seq_num and comando and args) == 0) or (comando not in acoes):
            resposta = str(seq_num) + " NOK"
            clientSocket.send(resposta.encode())
            clientSocket.close()
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
        else:
            if comando == "CUMP":
                if str(args) in clientes_validos:
                    resposta = str(seq_num) + " OK"
                    permissao = True
                    clientSocket.send(resposta.encode())
                else:
                    resposta = str(seq_num) + " NOK"
                    permissao = False
                    clientSocket.send(resposta.encode())
                    clientSocket.close()
                    clientSocket = socket(AF_INET, SOCK_STREAM)
                    clientSocket.connect((serverName, serverPort))

            if permissao is True:
                if comando == "LIST":
                    try:
                        for root, dirs, files in os.walk(".", topdown=False):
                            qtd = len(files)
                            if qtd!=0:
                                lista = ""
                                for name in files:
                                    lista += name + ","
                                lista=lista[:-1]
                                clientSocket.send((str(seq_num) + " ARQS " + str(qtd) + " " + lista).encode())
                            else:
                                resposta = str(seq_num) + " NOK"
                                clientSocket.send(resposta.encode())
                    except:
                        resposta = str(seq_num) + " NOK"
                        clientSocket.send(resposta.encode())

                if comando == "PEGA":
                    try:
                        tamanho = str(os.path.getsize(args))
                        f = open(args, 'rb')
                        arquivo = f.read()

                        clientSocket.send((str(seq_num) + " ARQ " + tamanho + " " ).encode()+arquivo)
                        f.close()
                    except:
                        resposta = str(seq_num) + " NOK"
                        clientSocket.send(resposta.encode())

                if comando == "TERM":
                    resposta = str(seq_num) + " OK"
                    clientSocket.send(resposta.encode())
                    permissao = False
                    clientSocket.close()
                    clientSocket = socket(AF_INET, SOCK_STREAM)
                    clientSocket.connect((serverName, serverPort))

            else:
                resposta = str(seq_num) + " NOK"
                clientSocket.send(resposta.encode())
    except Exception :
        traceback.print_exc(file=sys.stdout)
        break

clientSocket.close()