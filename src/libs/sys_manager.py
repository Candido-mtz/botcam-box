#!/usr/bin/python

import subprocess as sp
from message import Message

class SysManager:
    
    def __init__(self, cola):
        self.gets = {}
        self.gets[1] = self.getTemperatura
        self.cola = cola

    def procesar(self, msg):
        if msg.getTipoAlto() == 1:
            r = self.gets[msg.getSubtipo()]()
            self.cola.put ( Message(msg.getTipoBajo(), msg.getSubtipo(), r))
            return True
        elif msg.getTipoAlto() == 0:
            if msg.getSubtipo() == 2:
                print ( msg.getDatos())
                return True
            else:
                return False

    def getTemperatura(self):
        out = sp.check_output(['sensors'])
        out = out.splitlines()[2].split()[1]
        out = out[:-3]
        return str(float(out))

        
