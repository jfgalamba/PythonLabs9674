#!/usr/bin/env python3
"""
Permite descarregar imagens da API pública "https://api.thecatapi.com".
Esta versão utiliza o código gerado pelo designer da Qt. É síncrona
porque utiliza requests para fazer download do ficheiro (e todos os 
restantes meacanismos síncronos do Python). Em consequência disto, 
durante o processo de download das imagens, a aplicação fica pouco
"responsiva".
"""

from pathlib import Path
from urllib.parse import urlsplit

import PySide6.QtWidgets as qtw
from PySide6.QtWidgets import QMessageBox

import requests

# Alternativa A
import catpic_downloader_ui

# Alternativa B
# from PySide6.QtUiTools import loadUiType
# DesignerUiClass, QBaseClass = loadUiType('catpic_downloader.ui')  # type: ignore

# Alternativa B
# class MainWindow(QBaseClass, DesignerUiClass):

# Alternativa A
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
        progress_label = self.progress_label
        progress_label.setText("Searching...")
        self.download_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self._cancelled = False
        downloaded_count = 0
        try:
            for i in range(self.count_spin.value()):
                path, size = self._download_cat_image(i)
                downloaded_count += 1

                # Show progress
                progress_label.setText(f"Downloaded {path.name} with {size:,} bytes")
                qtw.QApplication.processEvents()
                if self._cancelled:
                    QMessageBox.information(self, "Cancelled", "Download cancelled")
                    return
        except requests.RequestException as ex:
            QMessageBox.critical(self, "Error", f"Error connecting to TheCatApi:\n{ex}")  # type: ignore
        finally:
            # Restore GUI initial state
            progress_label.setText(f"Done, {downloaded_count} cats downloaded")
            self.download_button.setEnabled(True)
            self.stop_button.setEnabled(False)
    #:

    def _download_cat_image(self, i: int) -> tuple[Path, int]:
        # Search
        # search_response = requests.get(MainWindow.CAT_API_URL)
        # search_response.raise_for_status()

        # # Download
        # url = search_response.json()[0]['url']
        # url = "https://live.staticflickr.com/65535/49956396262_ef41c1d9b0_o.jpg"

        url = f"http://localhost:8000/{i}.jpg"
        download_response = requests.get(url)

        # Save the contents of the image to a file
        # File path will be something like:
        #    i_cat.EXT
        # Where i is a number and EXT is the file extension
        parts = urlsplit(url)
        path = self.directory / f"{i:02}_cat{Path(parts.path).suffix}"
        path.write_bytes(download_response.content)
        return path, len(download_response.content)
    #:

    def on_cancel_button_clicked(self):
        self._cancelled = False
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
