import socket

HOST ='0.0.0.0'
PORT = 1111
BUFSIZ = 1024
ADDR = (HOST, PORT)


def aceitaSocket():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    server_socket.setsockopt( socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    while True:
        print('Server waiting for connection...')
        client_sock, addr = server_socket.accept()
        print('Client connected from: ', addr)
        while True:
            data = client_sock.recv(BUFSIZ)
            data = data.decode("utf-8")
            token = data.split(':')
            print(type(data))
            if  token[0].upper == 'END':
                break
            elif token[0].upper() == 'RANKING':
                print(" {} pediu rank".format(addr))
                client_sock.send("Ranking ta top".encode('utf-8'))
            elif token[0].upper() == 'NOME':
                print("{} chama-se {}".format(addr[0],token[1]))
                client_sock.send("ALGUEM".encode('utf-8'))
                pass 

            #print("Received from client: %s" % data.decode('utf-8'))
            print("Received from client {}: {}".format(addr[0],data))
            try:
                data = data.upper()
                print(data)
                client_sock.send(data.encode('utf-8'))
            except KeyboardInterrupt:
                print("Exited by user")
        client_sock.close()
    server_socket.close()

if __name__ == '__main__':
    aceitaSocket()


