import socket
from threading import Thread,Lock
import random
import sys

HOST ='0.0.0.0'
PORT = 1113
BUFSIZ = 1024
ADDR = (HOST, PORT)
lock_ranking = Lock()


class Ranking:
    
    def __init__(self):
        self.high_scores = []
    
    def add_highscore(self,highscore_novo):
        presente = False
        for highscore in self.high_scores:
            if(highscore[0] == highscore_novo[0]):
                highscore_atualizado = (highscore[0],(highscore[1]+highscore_novo[1]))
                self.high_scores.append(highscore_atualizado)
                self.high_scores.remove(highscore)
                presente = True
        if(not presente):
            self.high_scores.append(highscore_novo)
        self.sort()

    def sort(self):
        self.high_scores.sort(key=lambda tup: tup[1], reverse=True)
        
            

    # perguntar para o hugo, int isnt subscriptable(typeError)
    def __str__(self):
        string = ""

        for highscore in self.high_scores:
            string += "{}\t{} \n".format(str(highscore[1]),highscore[0])
        return string

 

def socketHandle(client_sock,addr):
    print('Client connected from: ', addr)
    while True:
        
        data = client_sock.recv(BUFSIZ).strip()
        data = data.decode("utf-8")
        token = data.split(':')
        
        if  token[0].upper() == 'END':
            break
        elif token[0].upper() == 'RANKING':
            print("OK - {} Pediu Rank".format(addr))
            client_sock.send(("\nRanking Geral\n\n{}\n\n".format(rank)).encode('utf-8'))
        elif token[0].upper() == 'NOME':
            print("{} chama-se {}".format(addr[0],token[1]))
            
            nome = token[1]
            numeros = []
            for x in range(5):
                numeros.append(random.randint(1,6))
            
            pontuacoes = []
            for numero in numeros:
                correspondencias=0
                for outronumero in numeros:
                    if(numero == outronumero):
                        correspondencias +=1
                pontuacoes.append(correspondencias)
            score=0
            if(max(pontuacoes) ==3):
                score=10
            elif(max(pontuacoes)==4):
                score=100
            elif(max(pontuacoes)==5):
                score=1000

            if score!=0:
                lock_ranking.acquire()
                
                highscore = (nome.upper(),score)
                rank.add_highscore(highscore)

                lock_ranking.release()
            else:
                pass

            response= "\n\nResultado da Partida\nDados Sorteados: {} \nPontuação: {}\n".format(numeros,score)
            print(numeros)
            client_sock.send(response.encode('utf-8'))

        
        print("Received from client {}: {}".format(addr[0],token))
        
        client_sock.close()
        sys.exit()
        
    
    

if __name__ == '__main__':
    # server setup
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    server_socket.setsockopt( socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    rank = Ranking()
    
    
    while True:
        opt = input("Configuração do servidor!\nDigite 1 para executar usando Threads, ou 2 para Processos.")
        if (opt == '1'):
            # threads
            while True:
                print("rank: {}\n".format(rank.high_scores))
                print('Server waiting for connection...{}'.format(PORT))
                client_sock, addr = server_socket.accept()
                t1 = Thread(target=socketHandle,args=(client_sock,addr))
                t1.start()
               

            pass
        elif(opt == '2'):
            # processos
            pass
        else:
            print("Opção Inválida!")
