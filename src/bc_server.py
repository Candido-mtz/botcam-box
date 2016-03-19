#!/usr/bin/python

import socket

s = socket.socket()
host = ''
port = 2014
s.bind((host, port))

s.listen(5)
print ("Escuchando en:", host,":" ,port)
while True:
        c, addr = s.accept()
        print ('Got connection from', addr)
        c.send('Thank you for connecting')
        c.close()
print 'bye'
