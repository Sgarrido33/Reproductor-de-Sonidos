DATA_FILE = "sounds_data.json"
import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog, QLineEdit, \
    QSlider, QHBoxLayout, QFileDialog, QMessageBox
import sys
from Ventana_Principal import Ui_MainWindow


class AddSoundDialog(QDialog): #Añadir sonido, heredado de QDialog
    def __init__(self, parent=None):
        super().__init__(parent)
        #Ventana
        self.setWindowTitle("Añadir Sonido")
        self.resize(400, 200)
        self.setGeometry(150, 150, 400, 250)

        layout = QVBoxLayout()

        #Nombre del sound
        self.name_input = QLineEdit(self) # Input nombre sound
        self.name_input.setPlaceholderText("Nombre del sonido")

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.name_input)

        #Subir archivo
        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
        self.file_input.setStyleSheet("background-color: lightgray;")

        self.file_button = QPushButton("Subir Archivo")
        self.file_button.clicked.connect(self.upload_file)

        layout.addWidget(QLabel("Archivo de audio:"))
        layout.addWidget(self.file_input)
        layout.addWidget(self.file_button)

        #Volumen TODO(añadir la funcionalidad para que funcione el play)
        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)

        layout.addWidget(QLabel("Volumen:"))
        layout.addWidget(self.volume_slider)

        #Hot key
        self.hotkey_input = QLineEdit(self) # TODO(añadir la funcionalidad luego de que funcione el play)
        self.hotkey_input.setPlaceholderText("Ej: Ctrl + A")

        layout.addWidget(QLabel("Combinación de teclas (opcional):"))
        layout.addWidget(self.hotkey_input)

        #Aceptar y Guardar
        btn_layout = QHBoxLayout()
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.clicked.connect(self.accept_sound)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        btn_layout.addWidget(self.accept_button)
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(["Archivos de Audio (*.mp3 *.wav)"])
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.file_input.setText(file_path)

    def accept_sound(self):
        if not self.name_input.text().strip() or not self.file_input.text().strip():
            QMessageBox.warning(self, "Campos vacíos", "Por favor, llena los campos de nombre y archivo antes de continuar.")
            return

        new_sound = {
            "name": self.name_input.text().strip(),
            "file": self.file_input.text().strip(),
            "volume": self.volume_slider.value(),
            "hotkey": self.hotkey_input.text().strip()
        }

        self.save_sound_to_json(new_sound)
        self.accept()

    def save_sound_to_json(self, sound_data):
        data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        data.append(sound_data)

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
