import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class Calcularw(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        uic.loadUi('cocopost.ui', self)

        self.pushButton.clicked.connect(self.calcular)
        self.label_25.setCursor(Qt.PointingHandCursor)
        self.label_25.mousePressEvent = self.regresar

        self.fec_combos = [
            self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_17, self.comboBox_18,
            self.comboBox_5, self.comboBox_6, self.comboBox_7,
            self.comboBox_9, self.comboBox_10, self.comboBox_11, self.comboBox_12, self.comboBox_13, self.comboBox_19,
            self.comboBox_14, self.comboBox_15, self.comboBox_16
        ]

        self.fec_combo_fac = [
            self.comboBox_20, self.comboBox_21, self.comboBox_22, self.comboBox_23, self.comboBox_24,
        ]

    def calcular_factores(self):
        valores_nivel_escala = {
            "PREC": {"Muy baja": 6.20, "Baja": 4.96, "Nominal": 3.72, "Alto ": 2.48, "Muy alto": 1.24, "Extra alto": 0.00},
            "FLEX": {"Muy baja": 5.07, "Baja": 4.05, "Nominal": 3.04, "Alto ": 2.03, "Muy alto": 1.01, "Extra alto": 0.00},
            "RESL": {"Muy baja": 7.07, "Baja": 5.65, "Nominal": 4.24, "Alto ": 2.83, "Muy alto": 1.41, "Extra alto": 0.00},
            "TEAM": {"Muy baja": 5.48, "Baja": 4.38, "Nominal": 3.29, "Alto ": 2.19, "Muy alto": 1.10, "Extra alto": 0.00},
            "PMAT": {"Muy baja": 7.80, "Baja": 6.24, "Nominal": 4.68, "Alto ": 3.12, "Muy alto": 1.56, "Extra alto": 0.00}
        }

        factores_escala = ["PREC", "FLEX", "RESL", "TEAM", "PMAT"]
        return sum(valores_nivel_escala[factor].get(combo.currentText(), 1) for combo, factor in zip(self.fec_combo_fac, factores_escala))

    def calcular_fec(self):
        valores_niveles = {
            "RSS": {"Muy baja": 0.75, "Baja": 0.88, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.40},
            "TDB": {"Muy baja": 1, "Baja": 0.94, "Nominal": 1, "Alto ": 1.08, "Muy alto": 1.16},
            "CPR": {"Muy baja": 0.70, "Baja": 0.85, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.30, "Extra alto": 1.65},
            "RUSE": {"Muy baja": 0.70, "Baja": 0.85, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.30, "Extra alto": 1.65},
            "DOC": {"Muy baja": 0.70, "Baja": 0.85, "Nominal": 1, "Alto ": 1.15, "Muy alto": 1.30, "Extra alto": 1.65},
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

        factores = ["RSS", "TDB", "CPR", "RTE", "RMP", "VMC", "TRC", "CAN", "EAN", "CPRO", "ESO", "ELP", "UTP", "UHC", "RLP"]
        return self.producto([valores_niveles[factor].get(combo.currentText(), 1) for combo, factor in zip(self.fec_combos, factores)])

    @staticmethod
    def producto(lista):
        resultado = 1
        for valor in lista:
            resultado *= valor
        return resultado

    def calcular(self):
        try:
            kldc = float(self.lineEdit_2.text())
            cpm = float(self.lineEdit.text())

            fec = self.calcular_fec()
            fac_escala = self.calcular_factores()

            esfuerzo = 2.94 * fec * (kldc ** (0.91 + (fac_escala/100)))
            tiempo = 3.67 * esfuerzo ** 0.33
            costo = esfuerzo * cpm

            self.label_21.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">Esfuerzo estimado: <span style=\" color:#ff0000;\">{esfuerzo:.2f} personas-mes</span></span></p></body></html>")
            self.label_22.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">Tiempo estimado de desarrollo: <span style=\" color:#ff0000;\">{tiempo:.2f} meses</span></span></p></body></html>")
            self.label_23.setText(f"<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">Costo estimado: <span style=\" color:#ff0000;\">${costo:.2f}</span></span></p></body></html>")

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos válidos para KLDC y CPM.")

    def regresar(self, event):
        if self.main_window:
            self.main_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Calcularw()
    d.show()
    sys.exit(app.exec_())