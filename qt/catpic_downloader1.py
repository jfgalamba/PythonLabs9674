#!/usr/bin/env python3
"""
Permite descarregar imagens da API pública "https://api.thecatapi.com".
Esta versão é síncrona e utiliza requests para HTTP/S.
"""

from pathlib import Path
from urllib.parse import urlsplit

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw
from PySide6.QtWidgets import QMessageBox
import requests


class MainWindow(qtw.QWidget):
    CAT_API_URL = "https://api.thecatapi.com/v1/images/search"

    def __init__(self, directory: Path,):
        super().__init__()

        # Initialize this MainWindow
        self.directory = directory
        self._cancelled = False
        self.setWindowTitle("Cat Downloader")
        self.setFixedSize(qtc.QSize(400, 200))

        # MainWindow layout
        main_layout = qtw.QVBoxLayout(self)
        main_layout.setSizeConstraint(qtw.QLayout.SizeConstraint.SetNoConstraint)

        # Let's add main layout contents, starting with a nested layout
        nested_layout = qtw.QFormLayout()
        nested_layout.setSizeConstraint(qtw.QLayout.SizeConstraint.SetNoConstraint)
        nested_layout.setFieldGrowthPolicy(qtw.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        main_layout.addLayout(nested_layout)

        # Counter to set the number of pics to download
        self.count_spin = count_spin = qtw.QSpinBox()
        count_spin.setValue(5)
        count_spin.setMinimum(1)
        count_spin_policy = qtw.QSizePolicy(
            qtw.QSizePolicy.Policy.Expanding,
            qtw.QSizePolicy.Policy.Fixed,
        )
        nested_layout.setLabelAlignment(
              qtc.Qt.AlignmentFlag.AlignLeading
            | qtc.Qt.AlignmentFlag.AlignLeft
            | qtc.Qt.AlignmentFlag.AlignVCenter
        )
        count_spin.setSizePolicy(count_spin_policy)
        nested_layout.addRow("How many cats?", count_spin)

        # Progress status
        self.progress_label = progress_label = qtw.QLabel("Idle. Click below to start downloading")
        progress_label.setStyleSheet(
            'QLabel {background-color: black; color: white; padding: 2px;}'
        )
        nested_layout.addRow("Status:", progress_label)

        # Control buttons
        self.download_button = download_button = qtw.QPushButton("Download")
        download_button.clicked.connect(self.on_download_button_clicked)
        main_layout.addWidget(download_button)

        self.stop_button = stop_button = qtw.QPushButton("Stop")
        stop_button.setEnabled(False)
        stop_button.clicked.connect(self.on_stop_button_clicked)
        main_layout.addWidget(stop_button)  

        self.hello_button = hello_button = qtw.QPushButton("Hello")
        hello_button.clicked.connect(self.on_hello_button_clicked)
        main_layout.addWidget(hello_button)

    #:

    def on_download_button_clicked(self):
        progress_label = self.progress_label
        progress_label.setText("Searching...")
        self.download_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        # qtw.QApplication.processEvents()

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
        search_response = requests.get(MainWindow.CAT_API_URL)
        search_response.raise_for_status()

        # # Download
        # url = search_response.json()[0]['url']
        # url = "https://live.staticflickr.com/65535/49956396262_ef41c1d9b0_o.jpg"
        url = "http://10.1.0.103:8000/data.bin"
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

    def on_stop_button_clicked(self):
        # QMessageBox.critical(self, "Aconteceu algo", "OLÁ!!")  # type: ignore
        self._cancelled = True
    #:

    def on_hello_button_clicked(self) -> None:
        qtw.QMessageBox.information(self, "Cumprimento", "Olá, tudo bem?")
    #:

#:

def main():
    import sys
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow(Path("."))
    main_window.show()     # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()
#:

if __name__ == '__main__':
    main()
