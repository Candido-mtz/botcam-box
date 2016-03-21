#!/usr/bin/python

import socket
import threading
import time
from multiprocessing import Queue
import libs.message as ms

class Server:
    def __init__(self):
        self.cola = Queue()
        self.sndr = None
        self.rcvr = None

    def receiver(self, client):
        print('Atendiendo')
        msg = ''
        while True:
            mm, msg = ms.getMessageFromClient(client, msg)
            if mm.getTipo() == 0:
                if mm.getSubtipo() == 1:
                    print ('Error al recivir dato')
                elif mm.getSubtipo() == 0:
                    self.cola.put(mm)
                    break
            elif mm.getTipo()== 1:
                print (mm.getDatos())
            else:
                pass
   
    def sender(self, client):
        while True:
            dato = self.cola.get()
            if dato.getTipo() == 0 and dato.getSubtipo() == 0:
                break
            fsend = str(dato)
            send = 0
            while send < len(fsend):
                ss = client.send(fsend[send:])
                if ss == 0:
                    raise "Error al enviar"
                send += ss
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


