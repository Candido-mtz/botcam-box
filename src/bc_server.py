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
        msg = ''
        while True:
            flag = False
            while not flag and len(msg)<10:
                dat = client.recv(1024)
                if not dat:
                    self.cola.put( Message(0, 0))
                    return
                msg += dat
                if not flag:
                    i = msg.find('>')
                    if i >= 0:
                        msg = msg[i+1:]
                        flag = True
                    else:
                        msg = ''
            tipo = int( msg[0:2])
            stipo = int(msg[2:4])
            lng = int(msg[4:10])
            msg = msg[10:]
            while len(msg) < (lng+2):
                dat = client.recv(min(lng+2-len(msg),2048))
                if (dat is None) or (len(dat) == 0):
                    self.cola.put(Message(0, 0))
                    return
                msg += dat;
            if msg[lng:lng+2] != ';;':
                print ('Error al recibir.')
                self.cola.put(Message(0, 0))
                return
            ds = msg[:lng]
            msg = msg[lng+2:]
            mm = Message(tipo, stipo, ds)
            print (str(mm))
            self.cola.put(mm)
    
    def sender(self, client):
        while True:
            dato = self.cola.get()
            if dato.getTipo() == 0 and dato.getSubtipo() == 0:
                break
            fsend = '>' + str(dato)
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


