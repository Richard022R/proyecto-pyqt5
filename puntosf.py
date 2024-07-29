import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow


class Pantalla(QMainWindow):
    def __init__(self):
        super(Pantalla, self).__init__()
        uic.loadUi('puntos.ui', self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Pantalla()
    d.show()
    sys.exit(app.exec_())
