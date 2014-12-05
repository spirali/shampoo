#
#    Copyright (C) 2014 Stanislav Bohm
#
#    This file is part of Shampoo.
#
#    Shampoo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    Shampoo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Shampoo.  If not, see <http://www.gnu.org/licenses/>.
#


from PyQt4.QtGui import QDialog, QLineEdit, \
                        QFormLayout, QPushButton, \
                        QHBoxLayout, QVBoxLayout


class ConfigDialog(QDialog):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Shampoo configuration")
        self.resize(400, 100)

        main_layout = QVBoxLayout()

        layout = QFormLayout()

        self.openfoam_path = QLineEdit()
        self.openfoam_path.setText(settings.value("openfoam/path"))
        layout.addRow("OpenFOAM path", self.openfoam_path)

        b_layout = QHBoxLayout()
        b_layout.addStretch(1)

        button = QPushButton("Ok")
        button.setDefault(True)
        button.clicked.connect(self.accept)
        b_layout.addWidget(button)


        main_layout.addLayout(layout)
        main_layout.addLayout(b_layout)
        self.setLayout(main_layout)

    def accept(self):
        self.settings.setValue("openfoam/path", self.openfoam_path.text())
        super().accept()
