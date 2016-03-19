#!/usr/bin/python

import socket
import threading
import time
from multiprocessing import Queue
from libs.message import Message

class Server:
    def __init__(self):
        self.cola = Queue()
        self.sndr = None
        self.rcvr = None

    def receiver(self, client):
        print('Atendiendo')
        time.sleep(10)
        self.cola.put(Message(1, 0, 'Thank you for connecting'))
        self.cola.put(Message(0, 0));
    
    def sender(self, client):
        while True:
            dato = self.cola.get()
            if dato.getTipo() == 0 and dato.getSubtipo() == 0:
                break
            client.send(str(dato))
        client.close()
        print('Conexion cerrada')

    def server(self):
        s = socket.socket()
        host = ''
        port = 2014
        s.bind((host,port))
        s.listen(2)
        print ('listening on port : % d' % port)
        while True:
            c, addr = s.accept()
            if not(self.rcvr is None):
                self.rcvr.join()
            self.sndr = threading.Thread(target=self.sender, args=(c,))
            self.sndr.setDaemon(True)
            self.sndr.start()
            self.rcvr = threading.Thread(target=self.receiver, args=(c,))
            self.rcvr.setDaemon(True)
            self.rcvr.start()

if __name__ == '__main__':
    srv = Server()
    srv.server()


