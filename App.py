import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog, QLineEdit, \
    QSlider, QHBoxLayout, QFileDialog, QMessageBox, QSizePolicy
import sys
from Add_Sound_Ventana import AddSoundDialog
from Ventana_Principal import Ui_MainWindow
from PyQt6 import QtWidgets
from PyQt6 import QtCore

DATA_FILE = "sounds_data.json"


class SoundBoard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.sounds = []
        self.next_id = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.load_sounds()

        #Desaparecer TitleBar y bordes
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgb(30, 30, 30);")

        # Funcionalidades de los botones
        self.ui.pushButton_3.clicked.connect(self.minimize_window)  #Minimize
        self.ui.pushButton.clicked.connect(self.maximize_restore_window)  #Maximize/Restore
        self.ui.pushButton_2.clicked.connect(self.close)  #Close

        self.is_maximized = False
        self.drag_pos = None
        self.titlebar = self.ui.Barra_Principal

    def minimize_window(self):
        self.showMinimized()

    def maximize_restore_window(self):
        if self.isMaximized():
            self.showNormal()
            self.is_maximized = False
        else:
            self.showMaximized()
            self.is_maximized = True

    def mousePressEvent(self, event):
        #Solo permite mover la ventana si se hace clic en la Barra_Principal
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.titlebar.underMouse():
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        #Mueve la ventana solo si se arrastra desde la Barra_Principal
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton and self.drag_pos and self.titlebar.underMouse():
            new_pos = self.pos() + (event.globalPosition().toPoint() - self.drag_pos)
            self.move(new_pos)
            self.drag_pos = event.globalPosition().toPoint()

        event.accept()


    def open_add_dialog(self):
        dialog = AddSoundDialog(self)

        # Para el next_id
        with open("sounds_data.json", "r", encoding="utf-8") as file:
            sounds_data = json.load(file)

        if sounds_data:
            self.next_id = max(sound['id'] for sound in sounds_data) + 1

        # New Sound
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_sound = {
                "name": dialog.name_input.text(),
                "file": dialog.file_input.text(),
                "volume": dialog.volume_slider.value(),
                "hotkey": dialog.hotkey_input.text()
            }

            # Solo agregamos a la lista y UI si no está vacío
            if new_sound["name"] and new_sound["file"]:
                new_sound['id'] = self.next_id
                self.add_sound(new_sound)
                self.save_sounds()  # Guardar cambios en el JSON

    # Boton de sound
    def add_sound(self, sound):
        self.sounds.append(sound)

        # Calculamos la posición en la cuadrícula
        index = len(self.sounds) - 1
        row = index // 2
        col = (index % 2) * 2

        # Creamos el botón de reproducción
        btn = QPushButton("▶")
        btn.setStyleSheet("font-size: 16px; padding: 10px;")
        btn.clicked.connect(lambda checked, s=sound: self.play_sound(s["id"], btn))

        label = QLabel(sound["name"])
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 14px; font-weight: bold;")

        if self.grid_layout is None:
            return

        self.grid_layout.addWidget(btn, row, col)
        self.grid_layout.addWidget(label, row, col + 1)

        if not hasattr(self, "buttons"):
            self.buttons = {}
        self.buttons[sound["id"]] = btn

    def play_sound(self, sound_id, btn):
        sound = next((s for s in self.sounds if s["id"] == sound_id), None)

        if btn.text() == "▶":
            print(f"Reproduciendo: {sound['file']}")
            btn.setText("⏹")  # Cambia a stop
        else:
            print(f"Deteniendo: {sound['file']}")
            btn.setText("▶")  # Cambia a play

    def save_sounds(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.sounds, file, indent=4)

    def load_sounds(self):
        # Limpieza de sonidos
        self.sounds = []

        if not os.path.exists("sounds_data.json"):
            with open("sounds_data.json", "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

        with open("sounds_data.json", "r", encoding="utf-8") as file:
            sounds_data = json.load(file)

        for sound in sounds_data:
            self.add_sound(sound)  # Llamar a add_sound() para mostrar en la UI


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SoundBoard()
    window.show()
    sys.exit(app.exec())
