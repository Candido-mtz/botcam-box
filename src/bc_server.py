#!/usr/bin/python

import socket
import threading
import time
from Queue import Queue

class Server:
    def __init__(self):
        self.cola = Queue()

    def receiver(self, client):
        pass
    
    def sender(self, client):
        print('Atendiendo')
        time.sleep(30)
        client.send('Thank you for connecting')
        print('Cerrando')
        client.close()

    def server(self):
        s = socket.socket()
        host = ''
        port = 2014
        s.bind((host,port))
        s.listen(2)
        print ('listening on port : % d' % port)
        while True:
            c, addr = s.accept()
            print ('Recibiendo conexion de %s' % str(addr))
            self.sndr = threading.Thread(target=self.sender, args=(c,))
            self.sndr.setDaemon(True)
            self.sndr.start()
            self.rcvr = threading.Thread(target=self.receiver, args=(c,))
            self.rcvr.setDaemon(True)
            self.rcvr.start()

if __name__ == '__main__':
    srv = Server()
    srv.server()


