import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog, QLineEdit, \
    QSlider, QHBoxLayout, QFileDialog
import sys

DATA_FILE = "sounds_data.json"


class AddSoundDialog(QDialog): #Añadir sonido, heredado de QDialog
    def __init__(self, parent=None):
        super().__init__(parent)
        #Ventana
        self.setWindowTitle("Añadir Sonido")
        self.setGeometry(150, 150, 400, 250)

        layout = QVBoxLayout()

        #Nombre del sound
        self.name_input = QLineEdit(self) # Input nombre sound
        self.name_input.setPlaceholderText("Nombre del sonido")

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.name_input)

        #Subir archivo TODO(que no haya errores xd)
        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
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
        self.hotkey_input.setPlaceholderText("Combinación de teclas opcional")

        layout.addWidget(QLabel("Combinación de teclas:"))
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

    #TODO(arreglar)
    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(["Archivos de Audio (mp3 o wav)"])
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.file_input.setText(file_path)

    #TODO(ARREGLAR)
    def accept_sound(self):
        if not self.name_input.text() or not self.file_input.text():
            print("Error: Nombre y archivo de audio obligatorios.")
            return
        self.accept()


class SoundBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.sounds = []
        self.initUI()
        self.load_sounds()

    def initUI(self):
        self.setWindowTitle("Sonidos")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        title = QLabel("Sonidos:")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        add_button = QPushButton("Añadir")
        add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(add_button)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)
        self.setLayout(layout)

    def open_add_dialog(self): #Completar
        dialog = AddSoundDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_sound = {
                "name": dialog.name_input.text(),
                "file": dialog.file_input.text(),
                "volume": dialog.volume_slider.value(),
                "hotkey": dialog.hotkey_input.text()
            }
            self.add_sound(new_sound)
            self.save_sounds()
        else:
            print("Cancelado")

    #Boton de sound
    def add_sound(self, sound):
        row = len(self.sounds) // 2
        col = (len(self.sounds) % 2) * 2
        btn = QPushButton("▶")
        btn.setStyleSheet("font-size: 16px; padding: 10px;")
        btn.clicked.connect(lambda checked, s=sound["name"]: self.play_sound(s))
        self.grid_layout.addWidget(btn, row, col)

        label = QLabel(sound["name"])
        self.grid_layout.addWidget(label, row, col + 1)

        self.sounds.append(sound)

    def play_sound(self, sound_name):
        print(f"Reproduciendo: {sound_name}")

    def save_sounds(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.sounds, file, indent=4)

    def load_sounds(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                self.sounds = json.load(file)
                for sound in self.sounds:
                    self.add_sound(sound)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SoundBoard()
    window.show()
    sys.exit(app.exec())