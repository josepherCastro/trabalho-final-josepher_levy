import sys
import os
import socket

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = input('Digite a porta do servidor:')
    BUFSIZ = 4096
    ADDR = (HOST,int(PORT))

    


    nome = input("digite seu nome\n")
    opt = " "
    os.system("clear")
    while(opt != "SAIR"):
        opt = input("[RANKING]\n[JOGAR]\n[SAIR]\n")
        if(opt.upper() == "JOGAR"):
            opt=""
            os.system("clear")
            while(opt == ""):
                
                opt=input("[ENTER]-jogar\n[Tecla+ENTER] - sair\n")
                if(opt != ""):
                    break
                os.system("clear")
                client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client_sock.connect(ADDR)
                dados = "nome:{}".format(nome)
                client_sock.send(dados.encode('utf-8'))
                resposta = client_sock.recv(BUFSIZ)
                resposta = resposta.decode('utf-8')
                print(resposta)
                client_sock.close()
            
                

        elif(opt.upper()=="SAIR"):
            os.system("clear")
            sys.exit()
        elif(opt.upper() == "RANKING"):
            os.system("clear")

            client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client_sock.connect(ADDR)
            dados = "ranking".encode('utf-8')
            client_sock.send(dados)
            resposta = client_sock.recv(BUFSIZ)
            resposta = resposta.decode('utf-8')
            print(resposta)
            client_sock.close()

            
