import os
import sys
import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt6 import QtWidgets, QtCore, QtGui

from Ventana_Principal import Ui_MainWindow

DATA_FILE = "sounds_data.json"


class SoundBoard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.sounds = []
        self.next_id = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_sounds()

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSpacing(10)  # Espaciado entre botones
        self.ui.frame_2.setLayout(self.grid_layout)

        self.column_count = 4  # Número máximo de columnas antes de hacer una nueva fila
        self.current_row = 0
        self.current_col = 0

        #Desaparecer TitleBar y bordes
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgb(30, 30, 30);")

        # Funcionalidades de los botones
        self.ui.pushButton_3.clicked.connect(self.minimize_window)  #Minimize
        self.ui.pushButton.clicked.connect(self.maximize_restore_window)  #Maximize/Restore
        self.ui.pushButton_2.clicked.connect(self.close)  #Close

        self.is_maximized = False
        self.dragging = False
        self.titlebar = self.ui.Barra_Principal

        # Redimension

        self._resizing = False
        self._margin = 10

        # Funcionalidad Boton Añadir

        self.ui.btn_add.clicked.connect(self.open_file)

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

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de audio", "",
                                                   "Archivos de Audio (*.mp3 *.wav)")
        if not file_path:
            return

        sound_name = os.path.basename(file_path)  # Nombre de archivo, nombre de sonido default

        existing_sounds = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                existing_sounds = json.load(file)

        if existing_sounds:
            self.next_id = max(sound["id"] for sound in existing_sounds) + 1
        else:
            self.next_id = 0

        new_sound = {
            "id": self.next_id,
            "name": sound_name,
            "file": file_path,
            "volume": 50,
            "hotkey": ""
        }

        self.save_sound_to_json(new_sound)
        self.add_sound_button(new_sound)
        QMessageBox.information(self, "Check", f"Sonido '{sound_name}' agregado correctamente.") # Lo quitare luego

        self.next_id += 1

    def save_sound_to_json(self, sound_data):
        data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

        data.append(sound_data)

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_sounds(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            sounds_data = json.load(file)

        for sound in sounds_data:
            self.add_sound_button(sound)

    def add_sound_button(self, sound):
        button = QPushButton(self.ui.frame_2)
        button.setFixedSize(70, 70)
        button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        icon_play = QtGui.QIcon("Images/play.jpg")
        button.setIcon(icon_play)
        button.setIconSize(QtCore.QSize(70, 70))

        # Pendiente de play_sound
        button.clicked.connect(lambda: self.play_sound(sound["file"]))

        max_length = 12
        display_name = (sound["name"][:max_length] + "...") if len(sound["name"]) > max_length else sound["name"]

        label = QLabel(display_name, self.ui.frame_2)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 12px; max-width: 140px;")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.ui.layout_frame_2.addLayout(layout)


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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SoundBoard()
    window.show()
    sys.exit(app.exec())
