from PyQt4 import QtCore, QtGui, uic
import sys
import socket
from multiprocessing import Queue
import logging
import libs.message as ms

class Sender(QtCore.QObject):
    #Esta signal sirve para invocar el quit del thread.
    finished = QtCore.pyqtSignal()
    def __init__(self, conex, cola):
        super(Sender, self).__init__()
        self.conex = conex
        self.cola = cola

    def sender(self):
        logging.debug('Comenzando envio de datos')
        while True:
            mm = self.cola.get()
            if mm.getTipo() == 0 and mm.getSubtipo() == 0:
                break
            fSend = str(mm)
            tsend = 0
            while tsend < len(fSend):
                ss = self.conex.send(fSend[tsend:])
                if ss == 0:
                    logging.debug('Error al enviar mensaje')
                    break
                tsend = tsend + ss
            if tsend < len(fSend):
                break
        logging.debug('Finalizando envio')
        self.finished.emit()

class Receiver(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    messagein = QtCore.pyqtSignal(int, int, QtCore.QString)
    def __init__(self, conex):
        super(Receiver, self).__init__()
        self.conex = conex

    def receiver(self):
        logging.debug('Comenzando recepcion de datos')
        msg = ''
        while True:
            mm, msg = ms.getMessageFromClient(self.conex, msg)
            if mm.getTipo() == 0 and mm.getSubtipo() == 0:
                break
            else:
                self.messagein.emit(mm.getTipo(), mm.getSubtipo(), QtCore.QString(mm.getDatos()))
        logging.debug('Finalizando recepcion')
        self.finished.emit()


class FrmCliente(QtGui.QMainWindow):
    def __init__(self):
        super(FrmCliente, self).__init__()
        uic.loadUi('rsrc/cliente.ui', self)
        self.btnConectar.clicked.connect(self.btnConectar_click)
        
    def btnConectar_click(self):
        if self.btnConectar.text() == 'Conectar':
            c = self.conectar()
            if c:
                self.btnConectar.setText('Desconectar')
        else:
            c = self.desconectar()
            if c:
                self.btnConectar.setText('Conectar')
    def desconectar(self):
        self.tmrTemp.stop()
        self.tSndr.quit()
        self.tRcvr.quit()
        self.conex.close()
        return True

    def conectar(self):
        srv = self.txtIP.text()
        conex = socket.socket()
        try:
            conex.connect((srv, 2014))
        except socket.error:
            print ('No se pudo conectar al servidor')
            return False
        self.conex = conex #guardamos la conexion
        self.colaEnvio = Queue()
        # Creando hilos
        logging.debug('Creando hilos')
        
        self.tSndr = QtCore.QThread()
        self.sndr = Sender(conex, self.colaEnvio)
        self.sndr.moveToThread(self.tSndr)
        self.tSndr.started.connect(self.sndr.sender)
        self.sndr.finished.connect(self.tSndr.quit)
        self.tSndr.start()

        self.tRcvr = QtCore.QThread()
        self.rcvr = Receiver(conex)
        self.rcvr.moveToThread(self.tRcvr)
        self.tRcvr.started.connect(self.rcvr.receiver)
        self.rcvr.finished.connect(self.tRcvr.quit)
        self.rcvr.messagein.connect(self.procesarMensaje)
        self.tRcvr.start()

        self.tmrTemp = QtCore.QTimer()
        self.tmrTemp.timeout.connect(self.pedirTemperatura)
        self.tmrTemp.start(1000)
        return True



    def pedirTemperatura(self):
        self.colaEnvio.put(ms.Message(11,1))

    def procesarMensaje(self, tipo, subtipo, datos):
        if tipo == 1:
            if subtipo == 1: #La temperatura
                self.txtTemp.setText(datos)
                

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, 
            format = '[%(levelname)s] - %(threadName)-10s : %(message)s')

    app = QtGui.QApplication(sys.argv)
    frm = FrmCliente()
    frm.show()
    sys.exit(app.exec_())
