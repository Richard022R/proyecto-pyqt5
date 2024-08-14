import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QDoubleSpinBox, QFileDialog, 
                             QMessageBox, QTabWidget, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal

class StyleHelper:
    @staticmethod
    def style_table(table):
        table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                border: 1px solid #d3d3d3;
                border-radius: 4px;
            }
            QTableWidget::item {
                border: 1px solid #d3d3d3;
            }
            QTableWidget::item:selected {
                background-color: #d3d3d3;
            }
        """)

    @staticmethod
    def style_button(button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #e6e6e6;
                border: 1px solid #d3d3d3;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d3d3d3;
            }
            QPushButton:pressed {
                background-color: #c3c3c3;
            }
        """)

class UCPCalculator(QMainWindow):

    switch_to_main = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Calculadora de Puntos de Caso de Uso")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.init_ui()

        # Añadir botón para volver al main
        self.back_to_main_button = QPushButton("Volver a la Pantalla Principal")
        StyleHelper.style_button(self.back_to_main_button)
        self.back_to_main_button.clicked.connect(self.go_back_to_main)
        self.layout.addWidget(self.back_to_main_button)
    
    def go_back_to_main(self):
        self.switch_to_main.emit()
        self.close()  # Cerrar la ventana de UCPCalculator

    def init_ui(self):
        # Crear pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #d3d3d3;
                background: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: #e6e6e6;
                border: 1px solid #d3d3d3;
                padding: 8px;
            }
            QTabBar::tab:selected {
                background: white;
            }
        """)
        self.layout.addWidget(self.tabs)

        # Pestaña de Actores y Casos de Uso
        self.actor_use_case_tab = QWidget()
        self.tabs.addTab(self.actor_use_case_tab, "Actores y Casos de Uso")
        self.actor_use_case_layout = QHBoxLayout(self.actor_use_case_tab)

        # Sección para Actores
        actors_group = QGroupBox("Actores")
        actors_layout = QVBoxLayout()
        self.actors_table = QTableWidget(0, 3)
        self.actors_table.setHorizontalHeaderLabels(["Actor", "Tipo", "Peso"])
        StyleHelper.style_table(self.actors_table)
        actors_layout.addWidget(self.actors_table)
        self.add_actor_button = QPushButton("Añadir Actor")
        self.add_actor_button.clicked.connect(self.add_actor)
        StyleHelper.style_button(self.add_actor_button)
        actors_layout.addWidget(self.add_actor_button)
        actors_group.setLayout(actors_layout)
        self.actor_use_case_layout.addWidget(actors_group)

        # Sección para Casos de Uso
        use_cases_group = QGroupBox("Casos de Uso")
        use_cases_layout = QVBoxLayout()
        self.use_cases_table = QTableWidget(0, 3)
        self.use_cases_table.setHorizontalHeaderLabels(["Caso de Uso", "Tipo", "Peso"])
        StyleHelper.style_table(self.use_cases_table)
        use_cases_layout.addWidget(self.use_cases_table)
        self.add_use_case_button = QPushButton("Añadir Caso de Uso")
        self.add_use_case_button.clicked.connect(self.add_use_case)
        StyleHelper.style_button(self.add_use_case_button)
        use_cases_layout.addWidget(self.add_use_case_button)
        use_cases_group.setLayout(use_cases_layout)
        self.actor_use_case_layout.addWidget(use_cases_group)

        # Pestaña de Factores Técnicos y Ambientales
        self.factors_tab = QWidget()
        self.tabs.addTab(self.factors_tab, "Factores")
        self.factors_layout = QVBoxLayout(self.factors_tab)

        # Factores Técnicos
        self.technical_factors_table = QTableWidget(13, 3)
        self.technical_factors_table.setHorizontalHeaderLabels(["Factor", "Peso", "Valor"])
        StyleHelper.style_table(self.technical_factors_table)
        self.factors_layout.addWidget(QLabel("Factores Técnicos:"))
        self.factors_layout.addWidget(self.technical_factors_table)

        # Factores Ambientales
        self.environmental_factors_table = QTableWidget(8, 3)
        self.environmental_factors_table.setHorizontalHeaderLabels(["Factor", "Peso", "Valor"])
        StyleHelper.style_table(self.environmental_factors_table)
        self.factors_layout.addWidget(QLabel("Factores Ambientales:"))
        self.factors_layout.addWidget(self.environmental_factors_table)

        self.init_factors_tables()

        # Botones para guardar y cargar
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar Proyecto")
        self.save_button.clicked.connect(self.save_project)
        StyleHelper.style_button(self.save_button)
        self.load_button = QPushButton("Cargar Proyecto")
        self.load_button.clicked.connect(self.load_project)
        StyleHelper.style_button(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        self.layout.addLayout(button_layout)

        # Botón para calcular
        self.calculate_button = QPushButton("Calcular")
        self.calculate_button.clicked.connect(self.calculate)
        StyleHelper.style_button(self.calculate_button)
        self.layout.addWidget(self.calculate_button)

        # Labels para mostrar resultados
        results_group = QGroupBox("Resultados")
        results_layout = QFormLayout()
        self.pcusa_label = QLabel()
        self.fct_label = QLabel()
        self.fa_label = QLabel()
        self.pcua_label = QLabel()
        self.effort_label = QLabel()
        results_layout.addRow("PCUSA:", self.pcusa_label)
        results_layout.addRow("FCT:", self.fct_label)
        results_layout.addRow("FA:", self.fa_label)
        results_layout.addRow("PCUA:", self.pcua_label)
        results_layout.addRow("Esfuerzo estimado:", self.effort_label)
        results_group.setLayout(results_layout)
        self.layout.addWidget(results_group)

    def init_factors_tables(self):
        technical_factors = [
            ("Sistema Distribuido", 2),
            ("Desempeño", 1),
            ("Eficiencia del usuario final (en-linea)", 1),
            ("Complejidad del procesamiento interno", 1),
            ("Reusabilidad del código", 1),
            ("Facilidad de instalación", 0.5),
            ("Facilidad de uso", 0.5),
            ("Portabilidad", 2),
            ("Facilidad de cambio", 1),
            ("Concurrencia", 1),
            ("Características especiales de seguridad", 1),
            ("Provee acceso a terceros", 1),
            ("Facilidades especiales de entrenamiento a los usuarios", 1)
        ]

        environmental_factors = [
            ("Familiaridad con el Proceso Unificado de Rational", 1.5),
            ("Experiencia en el desarrollo de aplicaciones", 0.5),
            ("Experiencia en Orientación a objetos", 1),
            ("Capacidad del jefe del proyecto", 0.5),
            ("Motivación", 1),
            ("Estabilidad de los requerimientos", 2),
            ("Personal a tiempo parcial", -1),
            ("Lenguaje de programación difícil", -1)
        ]

        for i, (factor, peso) in enumerate(technical_factors):
            self.technical_factors_table.setItem(i, 0, QTableWidgetItem(factor))
            self.technical_factors_table.setItem(i, 1, QTableWidgetItem(str(peso)))
            self.technical_factors_table.setCellWidget(i, 2, QSpinBox())
            self.technical_factors_table.cellWidget(i, 2).setRange(0, 5)

        for i, (factor, peso) in enumerate(environmental_factors):
            self.environmental_factors_table.setItem(i, 0, QTableWidgetItem(factor))
            self.environmental_factors_table.setItem(i, 1, QTableWidgetItem(str(peso)))
            self.environmental_factors_table.setCellWidget(i, 2, QSpinBox())
            self.environmental_factors_table.cellWidget(i, 2).setRange(0, 5)

    def add_actor(self):
        row_position = self.actors_table.rowCount()
        self.actors_table.insertRow(row_position)
        self.actors_table.setCellWidget(row_position, 1, QSpinBox())
        self.actors_table.cellWidget(row_position, 1).setRange(1, 3)
        self.actors_table.cellWidget(row_position, 1).valueChanged.connect(self.update_actor_weight)
        self.actors_table.setItem(row_position, 2, QTableWidgetItem("1"))

    def add_use_case(self):
        row_position = self.use_cases_table.rowCount()
        self.use_cases_table.insertRow(row_position)
        self.use_cases_table.setCellWidget(row_position, 1, QSpinBox())
        self.use_cases_table.cellWidget(row_position, 1).setRange(1, 3)
        self.use_cases_table.cellWidget(row_position, 1).valueChanged.connect(self.update_use_case_weight)
        self.use_cases_table.setItem(row_position, 2, QTableWidgetItem("5"))

    def update_actor_weight(self, value):
        sender = self.sender()
        if sender:
            row = self.actors_table.indexAt(sender.pos()).row()
            weight = 1 if value == 1 else (2 if value == 2 else 3)
            self.actors_table.setItem(row, 2, QTableWidgetItem(str(weight)))

    def update_use_case_weight(self, value):
        sender = self.sender()
        if sender:
            row = self.use_cases_table.indexAt(sender.pos()).row()
            weight = 5 if value == 1 else (10 if value == 2 else 15)
            self.use_cases_table.setItem(row, 2, QTableWidgetItem(str(weight)))

    def calculate(self):
        pa = sum(int(self.actors_table.item(row, 2).text()) for row in range(self.actors_table.rowCount()))
        pcu = sum(int(self.use_cases_table.item(row, 2).text()) for row in range(self.use_cases_table.rowCount()))
        pcusa = pa + pcu

        fct_sum = sum(float(self.technical_factors_table.item(row, 1).text()) * 
                      self.technical_factors_table.cellWidget(row, 2).value()
                      for row in range(self.technical_factors_table.rowCount()))
        fct = 0.6 + (0.01 * fct_sum)

        fa_sum = sum(float(self.environmental_factors_table.item(row, 1).text()) * 
                     self.environmental_factors_table.cellWidget(row, 2).value()
                     for row in range(self.environmental_factors_table.rowCount()))
        fa = 1.4 + (-0.03 * fa_sum)

        pcua = pcusa * fct * fa

        # Cálculo del esfuerzo
        x = sum(1 for row in range(6) if self.environmental_factors_table.cellWidget(row, 2).value() < 3)
        y = sum(1 for row in range(6, 8) if self.environmental_factors_table.cellWidget(row, 2).value() > 3)

        if x + y <= 2:
            effort_factor = 20
        elif x + y <= 4:
            effort_factor = 28
        else:
            effort_factor = 36

        effort = effort_factor * pcua

        self.pcusa_label.setText(f"PCUSA: {pcusa}")
        self.fct_label.setText(f"FCT: {fct:.2f}")
        self.fa_label.setText(f"FA: {fa:.2f}")
        self.pcua_label.setText(f"PCUA: {pcua:.2f}")
        self.effort_label.setText(f"Esfuerzo estimado: {effort:.2f} horas hombre")

    def save_project(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Proyecto", "", "JSON Files (*.json)")
        if filename:
            data = {
                "actors": [
                    {
                        "name": self.actors_table.item(row, 0).text() if self.actors_table.item(row, 0) else "",
                        "type": self.actors_table.cellWidget(row, 1).value(),
                        "weight": int(self.actors_table.item(row, 2).text())
                    }
                    for row in range(self.actors_table.rowCount())
                ],
                "use_cases": [
                    {
                        "name": self.use_cases_table.item(row, 0).text() if self.use_cases_table.item(row, 0) else "",
                        "type": self.use_cases_table.cellWidget(row, 1).value(),
                        "weight": int(self.use_cases_table.item(row, 2).text())
                    }
                    for row in range(self.use_cases_table.rowCount())
                ],
                "technical_factors": [
                    {
                        "name": self.technical_factors_table.item(row, 0).text(),
                        "weight": float(self.technical_factors_table.item(row, 1).text()),
                        "value": self.technical_factors_table.cellWidget(row, 2).value()
                    }
                    for row in range(self.technical_factors_table.rowCount())
                ],
                "environmental_factors": [
                    {
                        "name": self.environmental_factors_table.item(row, 0).text(),
                        "weight": float(self.environmental_factors_table.item(row, 1).text()),
                        "value": self.environmental_factors_table.cellWidget(row, 2).value()
                    }
                    for row in range(self.environmental_factors_table.rowCount())
                ]
            }
            with open(filename, 'w') as f:
                json.dump(data, f)

    def load_project(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Cargar Proyecto", "", "JSON Files (*.json)")
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.actors_table.setRowCount(0)
            for actor in data['actors']:
                self.add_actor()
                row = self.actors_table.rowCount() - 1
                self.actors_table.setItem(row, 0, QTableWidgetItem(actor['name']))
                self.actors_table.cellWidget(row, 1).setValue(actor['type'])
                self.actors_table.setItem(row, 2, QTableWidgetItem(str(actor['weight'])))

            self.use_cases_table.setRowCount(0)
            for use_case in data['use_cases']:
                self.add_use_case()
                row = self.use_cases_table.rowCount() - 1
                self.use_cases_table.setItem(row, 0, QTableWidgetItem(use_case['name']))
                self.use_cases_table.cellWidget(row, 1).setValue(use_case['type'])
                self.use_cases_table.setItem(row, 2, QTableWidgetItem(str(use_case['weight'])))

            for row, factor in enumerate(data['technical_factors']):
                self.technical_factors_table.cellWidget(row, 2).setValue(factor['value'])

            for row, factor in enumerate(data['environmental_factors']):
                self.environmental_factors_table.cellWidget(row, 2).setValue(factor['value'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = UCPCalculator()
    calculator.show()
    sys.exit(app.exec_())