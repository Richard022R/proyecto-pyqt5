import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from calcular import COCOMOIWindow
from calcularii import Calcularw
from puntos_caso_uso import UCPCalculator

class Pantalla(QMainWindow):
    def __init__(self):
        super(Pantalla, self).__init__()
        uic.loadUi('principal.ui', self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)
        
        # Desactivar el enfoque de los botones
        self.pushButton.setFocusPolicy(Qt.NoFocus)
        self.pushButton_1.setFocusPolicy(Qt.NoFocus)
        self.pushButton_2.setFocusPolicy(Qt.NoFocus)
        self.pushButton_3.setFocusPolicy(Qt.NoFocus)
        
        # Conectar los botones a sus respectivas funciones
        self.pushButton.clicked.connect(self.cocomo_i_clicked)
        self.pushButton_1.clicked.connect(self.cocomo_ii_clicked)
        self.pushButton_2.clicked.connect(self.info_clicked)
        self.pushButton_3.clicked.connect(self.puntosf_clicked)

    def cocomo_i_clicked(self):
        self.cocomop_i_window = COCOMOIWindow(self)
        self.cocomop_i_window.show()
        self.hide()  # Cerrar la ventana principal

    def cocomo_ii_clicked(self):
        print("COCOMO II button clicked")
        self.puntos_caso_de_uso = UCPCalculator(self)
        self.puntos_caso_de_uso.switch_to_main.connect(self.show)  # Conectar la señal a la función show de Pantalla
        self.puntos_caso_de_uso.show()
        self.hide()
        # Aquí puedes añadir la funcionalidad para COCOMO II

    def info_clicked(self):
        print("INFO button clicked")
        # Aquí puedes añadir la funcionalidad para Info

    def puntosf_clicked(self):
        self.pantalla_cocomo_ii = Calcularw(self)
        self.pantalla_cocomo_ii.show()
        self.hide()  # Cerrar la ventana principal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Pantalla()
    d.show()
    sys.exit(app.exec_())
