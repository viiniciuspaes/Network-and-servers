# -*- coding: utf8 -*-
# Author: Vinicius Paes
'''
README:
Executar em pyton 3.X.
Usuário válido: Vinícius.
'''

from socket import *
import os

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)  # conexoes podem ficar na fila

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")



permission = False
valid_clients = ["8610511023799105117115", "711089711799111"]
valid_commands = ["CUMP", "LIST", "PEGA", "TERM"]


def receive_msg():
    sentence = connectionSocket.recv(1024)
    sentence = sentence.decode()
    print(sentence)
    try:
        entry = sentence.split()
        seq_num = entry[0]
        command = entry[1]

        if command=="CUMP":
            args = ''.join(str(ord(c)) for c in entry[2])
        elif command=="PEGA":
            args = entry[2]
        else:
            args = ""
    except:
        return 0, 0, 0
    return seq_num,command,args


def list_cmd():
    for root, dirs, files in os.walk(".", topdown=False):
        n_files = len(files)
        if n_files != 0:
            lista = ""
            for name in files:
                lista += name + ", "
            lista = lista[:-1]
            connectionSocket.send((str(seq_num) + " ARQS " + str(n_files) + " " + str(root) +":" + " " + lista + "\n").encode())
        else:
            resposta = str(seq_num) + " NOK"
            connectionSocket.send(resposta.encode())


def pega_cmd(file):

    try:
        tamanho = str(os.path.getsize(file))
        f = open(file, 'rb')
        info = f.read()

        connectionSocket.send((str(seq_num) + " ARQ " + tamanho + "\n").encode() + info)
        f.close()
    except FileNotFoundError:
        resposta = str(seq_num) + " NOK"
        connectionSocket.send(resposta.encode())


def term_connection():
    resposta = str(seq_num) + " OK"
    connectionSocket.send(resposta.encode())
    connectionSocket.close()


def validate_user(user):
    if user in valid_clients:
        resposta = str(seq_num) + " OK"
        connectionSocket.send(resposta.encode())
        return True

    else:
        resposta = str(seq_num) + " NOK"
        connectionSocket.send(resposta.encode())
        connectionSocket.close()
        return False


connectionSocket, addr = serverSocket.accept()
while True:

    seq_num, comando, args = receive_msg()

    if((seq_num and comando and args) == 0) or (comando not in valid_commands):
        response = str(seq_num) + " NOK"
        connectionSocket.send(response.encode())
    else:
        if comando == "CUMP":
            permission = validate_user(args)

        if permission is True:
            if comando == "LIST":
                list_cmd()

            if comando == "PEGA":
                pega_cmd(args)

            if comando == "TERM":
                term_connection()
                permission = False
                break

        else:
            response = str(seq_num) + " NOK"
            connectionSocket.send(response.encode())

serverSocket.close()