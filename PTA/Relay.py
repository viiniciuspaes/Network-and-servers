# -*- coding: utf8 -*-

from socket import *

serverName = '127.0.0.1'
serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

clientPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.bind(('', clientPort))
clientSocket.listen(1)

print("Relay pronto para receber e retransmitir mensagens. Digite Ctrl+C para terminar.")
while True:
    try:

        connectionServer, addr = serverSocket.accept()
        connectionClient, addr = clientSocket.accept()

        while True:
            try:

                sentence, addr = connectionClient.recvfrom(2048)
                print(sentence.decode(),": Client request")

                if len(sentence)!=0:
                    try:
                        connectionServer.send(sentence)
                        try:
                            sentence, addr = connectionServer.recvfrom(1024)
                            if len(sentence)!=0:
                                print(sentence.decode(),": Retorno do servidor")
                                connectionClient.send(sentence)
                            else:
                                connectionClient.close()
                                connectionServer.close()
                                break
                        except:
                            connectionClient.close()
                            connectionServer.close()
                            break
                    except:
                        connectionClient.close()
                        connectionServer.close()
                        break
                else:
                    connectionClient.close()
                    connectionServer.close()
                    break
            except Exception as e:
                connectionClient.close()
                connectionServer.close()
                print(e)
                break
    except (KeyboardInterrupt, SystemExit):
        break