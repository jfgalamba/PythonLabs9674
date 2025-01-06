#!/usr/bin/env python3
"""
Permite descarregar imagens da API pública "https://api.thecatapi.com".
Esta versão utiliza o código gerado pelo designer da Qt.
"""

from pathlib import Path

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
from PySide6.QtWidgets import QMessageBox

import catpic_downloader_ui

class MainWindow(qtw.QWidget, catpic_downloader_ui.Ui_MainWindow):
    CAT_API_URL = "https://api.thecatapi.com/v1/images/search"

    def __init__(self, directory: Path):
        super().__init__()
        self.setupUi(self)

        # Initialize this MainWindow
        self.directory = directory
        self._cancelled = False

        # Connect signals
        self.download_button.clicked.connect(self.on_download_button_clicked)
        self.stop_button.clicked.connect(self.on_cancel_button_clicked)
        self.hello_button.clicked.connect(self.on_hello_button_clicked)
    #:

    def on_download_button_clicked(self):
        QMessageBox.information(self, "Download", "DOWNLOADING")
    #:

    def on_cancel_button_clicked(self):
        QMessageBox.information(self, "Cancel", "CANCELLATION")
    #:

    def on_hello_button_clicked(self) -> None:
        QMessageBox.information(self, "Cumprimento", "Olá, tudo bem?")
    #:
#:

def main():
    import sys
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow(Path('.'))
    main_window.show()

    # Start the event loop.
    app.exec()
#:

if __name__ == '__main__':
    main()
#:
