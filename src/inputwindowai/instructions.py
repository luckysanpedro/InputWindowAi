from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QComboBox, QDialog, QLabel, QLineEdit, QTextEdit, QDialogButtonBox

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)
        self.setStyleSheet("color: black; background-color: rgba(200, 200, 255, 0.9); border-radius: 5px;")

        self.setWindowTitle("Add Instructions")
        self.layout = QVBoxLayout(self)

        self.name_label = QLabel("Name")
        self.layout.addWidget(self.name_label)

        self.name_field = QLineEdit()
        self.name_field.setStyleSheet("color: black; background-color: rgba(200, 200, 255, 0.9); border-radius: 5px;")
        self.layout.addWidget(self.name_field)

        self.instructions_label = QLabel("Instructions")
        self.layout.addWidget(self.instructions_label)

        self.instructions_field = QTextEdit()
        self.instructions_field.setStyleSheet("color: black; background-color: rgba(200, 200, 255, 0.9); border-radius: 5px;")
        self.layout.addWidget(self.instructions_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
        
    def get_data(self):
        return self.name_field.text(), self.instructions_field.toPlainText()

class InstructionsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.instructions_dict = {}
        self.setAutoFillBackground(True)
        self.setStyleSheet("color: black; background-color: rgba(200, 200, 255, 0.9); border-radius: 5px;")

        self.layout = QHBoxLayout(self)

        self.add_button = QPushButton("Add Instructions")
        self.add_button.clicked.connect(self.add_instructions)
        self.layout.addWidget(self.add_button)

        self.dropdown = QComboBox()
        self.dropdown.setStyleSheet("color: black; background-color: rgba(200, 200, 255, 0.9);; border-radius: 5px;")
        self.layout.addWidget(self.dropdown)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_instructions)
        self.layout.addWidget(self.delete_button)

    def add_instructions(self):
        dialog = InstructionsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, instructions = dialog.get_data()
            self.dropdown.addItem(name)
            self.instructions_dict[name] = instructions

    def delete_instructions(self):
        current_text = self.dropdown.currentText()
        if current_text:
            index = self.dropdown.currentIndex()
            self.dropdown.removeItem(index)
            del self.instructions_dict[current_text]

    def get_current_instructions(self):
        current_name = self.dropdown.currentText()
        return self.instructions_dict.get(current_name, "")