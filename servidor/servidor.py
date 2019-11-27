import socket
from threading import Thread,Lock
import random
import sys
from multiprocessing import Process,Queue

HOST ='0.0.0.0'
PORT = 1113
BUFSIZ = 1024
ADDR = (HOST, PORT)
lock_ranking = Lock()


class Ranking:
    
    def __init__(self,lock):
        self.high_scores = []
        self.lock = lock
    
    def add_highscore(self,highscore_novo):
        self.lock.acquire()
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
        self.lock.release()

    def sort(self):
        self.high_scores.sort(key=lambda tup: tup[1], reverse=True)
        
    def __str__(self):
        string = ""

        for highscore in self.high_scores:
            string += "{}\t{} \n".format(str(highscore[1]),highscore[0])
        return string

class SocketHandleProcess(Process):
    def __init__(self,queue_highscores,client_sock,addr,rank):
        Process.__init__(self)
        self.queue_highscores = queue_highscores
        self.client_sock = client_sock
        self.addr = addr
        self.rank = rank
    def run(self):
        socketHandle(self.client_sock,self.addr,True,self.queue_highscores)

        
def rankingWatcher(queue_highscores):
    while True:
       rank.add_highscore(queue_highscores.get())



def socketHandle(client_sock,addr,flag_process,queue_highscores='none'):
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
                highscore = (nome.upper(),score)
                if(flag_process):
                    queue_highscores.put(highscore)
                    
                else:
                    rank.add_highscore(highscore)


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
    rank = Ranking(lock_ranking)
    
    
    while True:
        opt = input("Configuração do servidor!\nDigite 1 para executar usando Threads, ou 2 para Processos.")
        if (opt == '1'):
            # threads
            while True:
                print("rank: {}\n".format(rank.high_scores))
                print('Server waiting for connection...{}'.format(PORT))
                client_sock, addr = server_socket.accept()
                t1 = Thread(target=socketHandle,args=(client_sock,addr, False))
                t1.start()
               

            pass
        elif(opt == '2'):
            queue_highscores = Queue()
            t1 = Thread(target=rankingWatcher,args=[queue_highscores])
            t1.start()
            while True:
                print("rank: {}\n".format(rank.high_scores))
                print('Server waiting for connection...{}'.format(PORT))
                client_sock, addr = server_socket.accept()
                
                p1 = SocketHandleProcess(queue_highscores,client_sock,addr,rank.high_scores)
                p1.start()
        
            
        else:
            print("Opção Inválida!")
