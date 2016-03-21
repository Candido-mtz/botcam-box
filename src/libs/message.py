#!/usr/bin/python

def getMessageFromClient(client, msg):
    while True:
        flag = False
        while not (flag and len(msg)>=10):
            dat = client.recv(1024)
            if not dat:
                return (Message(0,0), msg)
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
                return (Message(0,0), msg)
            msg += dat;
        if msg[lng:lng+2] != ';;':
            return (Message(0,1), msg)
        ds = msg[:lng]
        msg = msg[lng+2:]
        return (Message(tipo, stipo, ds), msg)


class Message:
    
    def __init__(self, tipo, subtipo, datos=None):
        self.tipo = tipo
        self.subtipo = subtipo
        self.datos = datos

    def getTipoBajo(self):
        return self.tipo % 10

    def getTipoAlto(self):
        return int(self.tipo / 10)

    def getTipo(self):
        return self.tipo

    def getSubtipo(self):
        return self.subtipo

    def getDatos(self):
        return self.datos

    def getMessage(self):
        if(self.tipo > 99):
            raise 'El tipo solo puede ser de 0 a 99'
        if(self.subtipo >99):
            raise 'El subtipo solo puede ser de 0 a 99'
        if (self.datos is None) or (len(self.datos) == 0):
            return '>%02d%02d%06d;;' %(self.tipo, self.subtipo, 0)
        if len(self.datos) > 999999:
            raise 'Los datos enviados debe de ser menores a 1M'
        return '>%02d%02d%06d%s;;' % (self.tipo, self.subtipo, len(self.datos), self.datos)

    def __str__(self):
        return self.getMessage()

if __name__ == '__main__':
    m1 = Message(0,0)
    print str(m1)
    m2 = Message(1,3,'hola')
    print str(m2)

