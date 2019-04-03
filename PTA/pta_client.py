from socket import *


serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

mensagens_cnt = 0

# validando usuario no inicio da session
clientSocket.send((str(mensagens_cnt)+" CUMP "+ "Vinícius").encode())
modifiedMessage, addr = clientSocket.recvfrom(2048)
print("Autenticado:", modifiedMessage.decode())
mensagens_cnt += 1

while True:

    message = input('Informe sua mensagem:')

    clientSocket.send((str(mensagens_cnt)+" "+ message).encode())

    modifiedMessage, addr = clientSocket.recvfrom(2048)
    print("Retorno do Servidor:", modifiedMessage.decode())

    mensagens_cnt += 1

    if message == "TERM":
        break

clientSocket.close()

