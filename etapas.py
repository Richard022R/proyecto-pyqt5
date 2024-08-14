import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QLabel, QMessageBox

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        print("label_24 clicked!")
        self.clicked.emit()
        super().mousePressEvent(event)

class PantallaEtapas(QMainWindow):
    
    closed = pyqtSignal()  # Señal emitida cuando se cierra la ventana
    cpm_calculated = pyqtSignal(float)  # Nueva señal para enviar el CPM calculado

    def __init__(self, main_window = None):
        super(PantallaEtapas, self).__init__()
        self.main_window = main_window
        uic.loadUi('etapas.ui', self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

        # Reemplazar el QLabel con la clase ClickableLabel
        self.label_guardar = self.findChild(ClickableLabel, 'label_26')
        if self.label_guardar is None:
            self.label_guardar = ClickableLabel(self)
            self.label_guardar.setObjectName('label_26')
            self.label_guardar.setGeometry(410, 470, 141, 71)
            self.label_guardar.clicked.connect(self.show_cocomo)
        else:
            #self.label_info.setPixmap(self.label_info.pixmap())
            self.label_guardar.clicked.connect(self.show_cocomo)

        self.pushButton.clicked.connect(self.calcular)
        self.label_25.setCursor(Qt.PointingHandCursor)
        self.label_25.mousePressEvent = self.regresar


    def calcular(self):
        global lineas_codigo

        requerimientos_cantidad = float(self.lineEdit.text())
        planificacion_cantidad = float(self.lineEdit_2.text())
        analisis_cantidad = float(self.lineEdit_3.text())
        diseño_cantidad = float(self.lineEdit_4.text())
        programacion_cantidad = float(self.lineEdit_5.text())
        pruebas_cantidad = float(self.lineEdit_6.text())
        lanzamiento_cantidad = float(self.lineEdit_7.text())

        requerimientos_porcentaje = float(self.lineEdit_8.text())
        planificacion_porcentaje = float(self.lineEdit_11.text())
        analisis_porcentaje = float(self.lineEdit_9.text())
        diseño_porcentaje = float(self.lineEdit_10.text())
        programacion_porcentaje = float(self.lineEdit_13.text())
        pruebas_porcentaje = float(self.lineEdit_14.text())
        lanzamiento_porcentaje = float(self.lineEdit_12.text())

        porcentaje = requerimientos_porcentaje + planificacion_porcentaje + analisis_porcentaje + diseño_porcentaje + programacion_porcentaje + pruebas_porcentaje + lanzamiento_porcentaje

        if(porcentaje == 100):
            cpm = (requerimientos_cantidad * (requerimientos_porcentaje/100) +
                   planificacion_cantidad * (planificacion_porcentaje/100) +
                   analisis_cantidad * (analisis_porcentaje/100) + 
                   diseño_cantidad * (diseño_porcentaje/100) +
                   programacion_cantidad * (programacion_porcentaje/100) +
                   pruebas_cantidad * (programacion_porcentaje/100) +
                   lanzamiento_cantidad * (lanzamiento_porcentaje/100))
            print('CPM: ',cpm)
            self.cpm_calculated.emit(cpm)  # Emitir la señal con el valor calculado
            self.label_23.setText(f"<html><head/><body><p><span style=\" font-weight:500; color:#005500;\">CPM: {cpm:.2f}</span></p></body></html>")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese los porcentajes correctos, la suma de % debe ser 100%.")

    def show_cocomo(self):
        #with open('cpm.txt', 'w') as archivo:
        #    archivo.write(str(ldc))
        self.close()
    
    def closeEvent(self, event):
        self.closed.emit()  # Emitir la señal al cerrar la ventana
        event.accept()  # Aceptar el evento de cierre

    def regresar(self, event):
        #self.main_window.show()  # Muestra la ventana principal
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = PantallaEtapas()
    d.show()
    sys.exit(app.exec_())