import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QLabel

class Pantallaf(QMainWindow):
    def __init__(self):
        super(Pantallaf, self).__init__()
        uic.loadUi('puntos.ui', self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

        # Connect signals
        self.spinBox.valueChanged.connect(self.tabla)
        for i in range(2, 16):
            spinbox = getattr(self, f'spinBox_{i}')
            spinbox.valueChanged.connect(self.tabla)

        self.radioButton.toggled.connect(self.activar)
        self.radioButton_2.toggled.connect(self.activar)
        self.pushButton.clicked.connect(self.calcular)

        self.tabla()
        self.activar()

    def tabla(self):
        resultado1 = self.spinBox.value() * 7 + self.spinBox_8.value() * 5 + self.spinBox_13.value() * 4
        resultado2 = self.spinBox_2.value() * 6 + self.spinBox_9.value() * 4 + self.spinBox_14.value() * 3
        resultado3 = self.spinBox_3.value() * 6 + self.spinBox_7.value() * 4 + self.spinBox_12.value() * 3
        resultado4 = self.spinBox_4.value() * 10 + self.spinBox_6.value() * 7 + self.spinBox_11.value() * 5
        resultado5 = self.spinBox_5.value() * 10 + self.spinBox_10.value() * 7 + self.spinBox_15.value() * 5

        self.label_13.setText(str(resultado1))
        self.label_14.setText(str(resultado2))
        self.label_15.setText(str(resultado3))
        self.label_16.setText(str(resultado4))
        self.label_17.setText(str(resultado5))

        total = resultado1 + resultado2 + resultado3 + resultado4 + resultado5
        self.label_19.setText(str(total))

    def lenguajes(self):
        return {
            "AGL4": 40, "Ada83": 71, "Ada95": 49, "APL": 32,
            "BASIC-compilado": 91, "BASIC-interpretado": 128,
            "BASIC ANSI/Quick/Turbo": 64, "C": 128, "C++": 29,
            "Clipper": 19, "Cobol ANSI 85": 91, "Delphi 1": 29,
            "Ensamblador": 320, "Ensamblador (Macro)": 213,
            "Forth": 64, "Fortran 77": 105, "FoxPro 2.5": 34,
            "Java": 53, "Modula 2": 80, "Oracle": 40,
            "Oracle 2000": 23, "Paradox": 36, "Pascal": 91,
            "Pascal Turbo 5": 45, "Power Builder": 16, "Prolog": 64,
            "Visual Basic 3": 32, "Visual C++": 34, "Visual Cobol": 20
        }

    def activar(self):
        if self.radioButton.isChecked():
            self.comboBox.setEnabled(True)
            self.textEdit.setEnabled(False)
            self.textEdit_2.setEnabled(False)
        elif self.radioButton_2.isChecked():
            self.comboBox.setEnabled(False)
            self.textEdit.setEnabled(True)
            self.textEdit_2.setEnabled(True)

    def calcular(self):
        total = float(self.label_19.text())
        if self.radioButton.isChecked():
            lenguaje = self.comboBox.currentText()
            factor = self.lenguajes().get(lenguaje, 1)
        else:
            factor = float(self.textEdit_2.toPlainText() or 1)
        
        resultado = total * factor
        self.label_24.setText(f"{resultado:.2f}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Pantallaf()
    d.show()
    sys.exit(app.exec_())