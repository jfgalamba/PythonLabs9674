# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'catpic_downloader.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QPushButton,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(400, 200))
        MainWindow.setMaximumSize(QSize(400, 200))
        self.verticalLayout = QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nested_layout = QFormLayout()
        self.nested_layout.setObjectName(u"nested_layout")
        self.nested_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.nested_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.nested_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.count_label = QLabel(MainWindow)
        self.count_label.setObjectName(u"count_label")

        self.nested_layout.setWidget(0, QFormLayout.LabelRole, self.count_label)

        self.count_spin = QSpinBox(MainWindow)
        self.count_spin.setObjectName(u"count_spin")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.count_spin.sizePolicy().hasHeightForWidth())
        self.count_spin.setSizePolicy(sizePolicy1)

        self.nested_layout.setWidget(0, QFormLayout.FieldRole, self.count_spin)

        self.status_label = QLabel(MainWindow)
        self.status_label.setObjectName(u"status_label")

        self.nested_layout.setWidget(1, QFormLayout.LabelRole, self.status_label)

        self.progress_label = QLabel(MainWindow)
        self.progress_label.setObjectName(u"progress_label")
        self.progress_label.setStyleSheet(u"QLabel {\n"
"	background-color: black;\n"
"   	color: white;\n"
"	padding: 2px;\n"
"}\n"
"")

        self.nested_layout.setWidget(1, QFormLayout.FieldRole, self.progress_label)


        self.verticalLayout.addLayout(self.nested_layout)

        self.download_button = QPushButton(MainWindow)
        self.download_button.setObjectName(u"download_button")

        self.verticalLayout.addWidget(self.download_button)

        self.stop_button = QPushButton(MainWindow)
        self.stop_button.setObjectName(u"stop_button")

        self.verticalLayout.addWidget(self.stop_button)

        self.hello_button = QPushButton(MainWindow)
        self.hello_button.setObjectName(u"hello_button")

        self.verticalLayout.addWidget(self.hello_button)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cat Downloader", None))
        self.count_label.setText(QCoreApplication.translate("MainWindow", u"How many cats?", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.progress_label.setText(QCoreApplication.translate("MainWindow", u"IIdle. Click to start downloading", None))
        self.download_button.setText(QCoreApplication.translate("MainWindow", u"Download!", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.hello_button.setText(QCoreApplication.translate("MainWindow", u"Hello", None))
    # retranslateUi

