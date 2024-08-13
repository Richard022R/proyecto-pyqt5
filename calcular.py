import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from puntosf import Pantallaf

esfuerzo = None
tipo_proyecto = None
kldc = None
fec = None
tiempo = None
cpm = None
ldc = None
contenido_global = None

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        print("label_24 clicked!")
        self.clicked.emit()
        super().mousePressEvent(event)

class ClickableLabel2(QLabel):
    clicked2 = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel2, self).__init__(parent)

    def mousePressEvent(self, event):  # Asegúrate de que el método se llame mousePressEvent
        print("label_26 clicked!")  # Depura si se detecta el clic
        self.clicked2.emit()
        print("clicked2 signal emitted")
        super().mousePressEvent(event)

class COCOMOIWindow(QMainWindow):
    def __init__(self, main_window=None):
        super(COCOMOIWindow, self).__init__()
        self.main_window = main_window
        uic.loadUi('D:/cocomo/proyecto-pyqt5/cocomop.ui', self)

        # Reemplazar el QLabel con la clase ClickableLabel
        self.label_c3 = self.findChild(ClickableLabel, 'label_24')
        if self.label_c3 is None:
            self.label_c3 = ClickableLabel(self)
            self.label_c3.setObjectName('label_24')
            self.label_c3.setGeometry(590, 580, 61, 61)
            self.label_c3.clicked.connect(self.show_info)
        else:
            #self.label_info.setPixmap(self.label_info.pixmap())
            self.label_c3.clicked.connect(self.show_info)

        # Reemplazar el QLabel con la clase ClickableLabel
        self.label_puntosfuncion = self.findChild(ClickableLabel2, 'label_26')
        
        if self.label_puntosfuncion is None:
            self.label_puntosfuncion = ClickableLabel2(self)
            self.label_puntosfuncion.setObjectName('label_26')
            self.label_puntosfuncion.setGeometry(600, 10, 91, 81)
            self.label_puntosfuncion.clicked2.connect(self.show_info2)
        else:
            self.label_puntosfuncion.clicked2.connect(self.show_info2)

        print('puntos de funcion: ',type(self.label_puntosfuncion))
        print('ecuaciones: ',type(self.label_c3))

        # Conectar el botón de cálculo a su función
        self.pushButton.clicked.connect(self.calcular)
        self.label_25.setCursor(Qt.PointingHandCursor)
        self.label_25.mousePressEvent = self.regresar

        # Inicializar los comboboxes de factores
        self.fec_combos = [
            self.comboBox_2, self.comboBox_3, self.comboBox_4,  # Productos
            self.comboBox_5, self.comboBox_6, self.comboBox_7, self.comboBox_8,  # Plataforma
            self.comboBox_9, self.comboBox_10, self.comboBox_11, self.comboBox_12, self.comboBox_13,  # Persona
            self.comboBox_14, self.comboBox_15, self.comboBox_16  # Proyecto
        ]

        # Inicializar valores
        self.factores = {
            'Orgánico': {'a': 3.2, 'b': 1.05, 'c': 2.5, 'd': 0.38},
            'Moderado': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
            'Embebido': {'a': 2.8, 'b': 1.20, 'c': 2.5, 'd': 0.32}
        }

    def calcular_fec(self):
        valores_niveles = {
            "RSS": {"Muy baja": 0.75, "Baja": 0.88, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.40},
            "TDB": {"Muy baja": 1, "Baja": 0.94, "Nominal": 1, "Alto ": 1.08, "Muy alto": 1.16},
            "CPR": {"Muy baja": 0.70, "Baja": 0.85, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.30, "Extra alto": 1.65},
            "RTE": {"Nominal": 1, "Alto ": 1.11, "Muy alto": 1.30, "Extra alto": 1.66},
            "RMP": {"Muy baja": 1, "Baja": 1, "Nominal": 1, "Alto ": 1.06, "Muy alto": 1.21, "Extra alto": 1.56},
            "VMC": {"Baja": 0.87, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.30},
            "TRC": {"Nominal": 1, "Alto ": 1.07, "Muy alto": 1.15},
            "CAN": {"Muy baja": 1.46, "Baja": 1.19, "Nominal": 1, "Alto ": 0.86, "Muy alto": 0.71},
            "EAN": {"Muy baja": 1.29, "Baja": 1.13, "Nominal": 1, "Alto ": 0.91, "Muy alto": 0.82},
            "CPRO": {"Muy baja": 1.42, "Baja": 1.17, "Nominal": 1, "Alto ": 0.86, "Muy alto": 0.70},
            "ESO": {"Muy baja": 1.21, "Baja": 1.10, "Nominal": 1, "Alto ": 0.90},
            "ELP": {"Muy baja": 1.14, "Baja": 1.07, "Nominal": 1, "Alto ": 0.95},
            "UTP": {"Muy baja": 1.24, "Baja": 1.10, "Nominal": 1, "Alto ": 0.91, "Muy alto": 0.82},
            "UHC": {"Muy baja": 1.24, "Baja": 1.10, "Nominal": 1, "Alto ": 0.91, "Muy alto": 0.83},
            "RLP": {"Muy baja": 1.23, "Baja": 1.08, "Nominal": 1, "Alto ": 1.04, "Muy alto": 1.10}
        }

        fec = 1
        factores = ["RSS", "TDB", "CPR", "RTE", "RMP", "VMC", "TRC", "CAN", "EAN", "CPRO", "ESO", "ELP", "UTP", "UHC", "RLP"]
        for combo, factor in zip(self.fec_combos, factores):
            nivel = combo.currentText()
            fec *= valores_niveles[factor].get(nivel, 1)
        return fec

    def calcular(self):
        global esfuerzo, tipo_proyecto, kldc, fec, tiempo, cpm, contenido_global
        try:
            kldc = float(self.lineEdit_2.text())
            cpm = float(self.lineEdit.text())
            tipo_proyecto = self.comboBox.currentText()

            factores = self.factores[tipo_proyecto]
            fec = self.calcular_fec()

            esfuerzo = factores['a'] * (kldc ** factores['b']) * fec
            tiempo = factores['c'] * (esfuerzo ** factores['d'])
            costo = esfuerzo * cpm

            self.label_21.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">Esfuerzo estimado: <span style=\" color:#ff0000;\">{esfuerzo:.2f} personas-mes</span></span></p></body></html>")
            self.label_22.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">Tiempo estimado de desarrollo: <span style=\" color:#ff0000;\">{tiempo:.2f} meses</span></span></p></body></html>")
            self.label_23.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">Costo estimado: <span style=\" color:#ff0000;\">${costo:.2f}</span></span></p></body></html>")

            # Pasa los valores calculados a la ventana de información
            #self.info_window = COCOMOIinfo(esfuerzo, tipo_proyecto, kldc, fec, tiempo, cpm)
            #self.info_window.show()

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos válidos para KLDC y CPM.")

    def show_info(self):
        self.info_window = COCOMOIinfo(esfuerzo, tipo_proyecto, kldc, fec, tiempo, cpm)
        self.info_window.show()

    def show_info2(self):
        global contenido_global
        self.pantalla_puntosf = Pantallaf()
        self.pantalla_puntosf.closed.connect(self.actualizar_lineEdit_contenido)
        self.pantalla_puntosf.show()
        with open('cpm.txt', 'r') as archivo:
            contenido = archivo.read()
            print('contenido: ', contenido)
        contenido_global = contenido
        self.lineEdit.setText(contenido)

    def regresar(self, event):
        if self.main_window:
            self.main_window.show()  # Muestra la ventana principal si existe
        self.close()

    def actualizar_lineEdit_contenido(self):
        try:
            with open('cpm.txt', 'r') as archivo:
                contenido = archivo.read()
                print('Contenido leído: ', contenido)
            self.lineEdit.setText(contenido)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No se encontró el archivo cpm.txt.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Ocurrió un error al leer el archivo: {e}")
    
class COCOMOIinfo(QMainWindow):
    def __init__(self, esfuerzo=None, tipo_proyecto=None, kldc=None, fec=None, tiempo=None, cpm=None, parent=None):
        super(COCOMOIinfo, self).__init__()
        uic.loadUi('D:/cocomo/proyecto-pyqt5/ecuaciones.ui', self)

        self.resize(734, 684)

        if tipo_proyecto == 'Orgánico':
            tipo = 3.2
            exp = 1.05
            exp_2 = 0.38

        if tipo_proyecto == 'Moderado':
            tipo = 3.0
            exp = 1.12
            exp_2 = 0.35

        if tipo_proyecto == 'Embebido':
            tipo = 2.8
            exp = 1.20
            exp_2 = 0.32

        if esfuerzo is not None:
            print('Esfuerzo: ', esfuerzo)
            self.show_esfuerzo(esfuerzo, tipo, exp, kldc, fec)
        if tiempo is not None:
            print('Tiempo: ', tiempo)
            self.show_tiempo(tiempo, exp_2, esfuerzo)
        if cpm is not None:
            print('CPM: ', cpm)
            self.show_costo(esfuerzo, cpm)
        if tipo_proyecto is not None:
            print('Tipo proyecto: ', tipo_proyecto)
        if kldc is not None:
            print('KLDC: ', kldc)
        if fec is not None:
            print('FEC: ', fec)

        self.label_13.setText(f"<html><head/><body><p><span style=\" font-weight:600; font-style:italic; color:#005500;\">Tipo de Proyecto: {tipo_proyecto}</span></p></body></html>")

    def show_esfuerzo(self, esfuerzo, tipo, exp, kldc, fec):
        # Asume que tienes un QLabel con el nombre 'label_esfuerzo' en ecuaciones.ui
        self.label_7.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">ESF = {tipo:.2f} * (KLDC) ^ {exp:.2f} * FEC</span></p></body></html>")
        self.label_10.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">ESF = {tipo:.2f} * ({kldc:.2f}) ^ {exp:.2f} * {fec:.2f}</span></p></body></html>")
        self.label_11.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">ESF = {tipo:.2f} * ({kldc ** exp:.2f}) * {fec:.2f}</span></p></body></html>")
        self.label_12.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">ESF = {esfuerzo:.2f}</span></p></body></html>")

    def show_tiempo(self, tiempo, exp_2, esfuerzo):
        self.label_8.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">TDES = 2.5 * (ESF) ^ {exp_2:.2f}</span></p></body></html>")
        self.label_14.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">TDES = 2.5 * ({esfuerzo:.2f}) ^ {exp_2:.2f}</span></p></body></html>")
        self.label_15.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">TDES = 2.5 * ({esfuerzo ** exp_2:.2f})</span></p></body></html>")
        self.label_16.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">TDES = {tiempo:.2f}</span></p></body></html>")

    def show_costo(self, esfuerzo, cpm):
        self.label_9.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">C = ESF * CPM</span></p></body></html>")
        self.label_17.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">C = {esfuerzo:.2f} ^ {cpm:.2f}</span></p></body></html>")
        self.label_18.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">C = {esfuerzo * cpm:.2f}</span></p></body></html>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = COCOMOIWindow()
    d.show()
    sys.exit(app.exec_())