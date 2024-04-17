import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from schemdraw import Drawing
from schemdraw.elements import Resistor, Capacitor, Inductor, Line

class LCFilter(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Draw LC filter schematic
        self.draw_schematic()

    def draw_schematic(self):
        d = Drawing(unit=0.1)  # Set unit to adjust size
        d += Resistor().label('$R$')
        d += Line().right().length(5)
        
        d += Inductor().label('$L$')
        d += Line().right().length(3)
        d += Line().down().length(1)
        d += Capacitor().label('$C$')
        d += Line().down().length(1)
        # Connect ends to close the circuit
        d += Line().left().length(3)
        d.push()
        d += Line().down().length(0.5)
        d.pop()
        
        # Save the schematic to SVG
        d.save('schematic.svg')
        
        # Display the schematic
        label = QLabel()
        pixmap = QPixmap("schematic.svg")
        label.setPixmap(pixmap)
        self.layout.addWidget(label)

class ParametersPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.component_labels = {}
        self.component_values = {}

        components = ['L', 'C']
        for component in components:
            label = QLabel(component)
            layout.addWidget(label)
            self.component_labels[component] = label

            value_edit = QLineEdit()
            value_edit.textChanged.connect(lambda text, comp=component: self.update_component_value(comp, text))
            layout.addWidget(value_edit)
            self.component_values[component] = value_edit

    def update_component_value(self, component, value):
        print(f"{component}: {value}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LC Filter GUI")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        self.lc_filter = LCFilter()
        layout.addWidget(self.lc_filter)

        self.parameters_panel = ParametersPanel()
        layout.addWidget(self.parameters_panel)

        # Export button
        export_button = QPushButton("Export Parameters")
        export_button.clicked.connect(self.export_parameters)
        layout.addWidget(export_button)

    def export_parameters(self):
        parameters = {}
        for component, value_edit in self.parameters_panel.component_values.items():
            parameters[component] = value_edit.text()
        with open('parameters.json', 'w') as f:
            json.dump(parameters, f)
        print("Parameters exported successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
