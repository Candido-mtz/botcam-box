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


class FrmCliente(QtGui.QMainWindow):
    def __init__(self):
        super(FrmCliente, self).__init__()
        uic.loadUi('rsrc/cliente.ui', self)
        self.btnConectar.clicked.connect(self.btnConectar_click)
        
    def btnConectar_click(self):
        srv = self.txtIP.text()
        conex = socket.socket()
        try:
            conex.connect((srv, 2014))
        except socket.error:
            print ('No se pudo conectar al servidor')
            return

        self.colaEnvio = Queue()
        # Creando hilos
        logging.debug('Creando hilos')
        self.tSndr = QtCore.QThread()
        self.sndr = Sender(conex, self.colaEnvio)
        self.sndr.moveToThread(self.tSndr)
        self.tSndr.started.connect(self.sndr.sender)
        self.sndr.finished.connect(self.tSndr.quit)
        self.tSndr.start()
        self.colaEnvio.put(ms.Message(1,2,'Hola mundo del servidor'))


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, 
            format = '[%(levelname)s] - %(threadName)-10s : %(message)s')

    app = QtGui.QApplication(sys.argv)
    frm = FrmCliente()
    frm.show()
    sys.exit(app.exec_())
