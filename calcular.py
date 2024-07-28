import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class COCOMOIWindow(QMainWindow):
    def __init__(self):
        super(COCOMOIWindow, self).__init__()
        uic.loadUi('cocomop.ui', self)
        
        # Conectar el botón de cálculo a su función
        self.pushButton.clicked.connect(self.calcular)

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


        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos válidos para KLDC y CPM.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = COCOMOIWindow()
    d.show()
    sys.exit(app.exec_())