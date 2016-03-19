#!/usr/bin/python
class Message:
    
    def __init__(self, tipo, subtipo, datos=None):
        self.tipo = tipo
        self.subtipo = subtipo
        self.datos = datos

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
        if self.datos is None:
            return '%02d%02d%06d;;' %(self.tipo, self.subtipo, 0)
        if len(self.datos) > 999999:
            raise 'Los datos enviados debe de ser menores a 1M'
        return '%02d%02d%06d%s;;' % (self.tipo, self.subtipo, len(self.datos), self.datos)

    def __str__(self):
        return self.getMessage()

if __name__ == '__main__':
    m1 = Message(0,0)
    print str(m1)
    m2 = Message(1,3,'hola')
    print str(m2)

