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

from base.events import Signal

from PyQt4.QtGui import QPlainTextEdit, QTextCharFormat
from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt


class Console(QPlainTextEdit):


    def __init__(self):
        super().__init__()
        self.setStyleSheet("font: 10pt \"Monospace\";")
        self.setReadOnly(True)
        self.process = None
        self.errorformat = QTextCharFormat()
        self.errorformat.setForeground(Qt.red)

        self.on_finished = Signal()

    def set_process(self, process):
        assert self.process is None
        self.process = process
        process.setParent(self)
        process.readyReadStandardOutput.connect(self.write_stdout)
        process.readyReadStandardError.connect(self.write_stderr)
        process.error.connect(self.show_error)
        process.finished.connect(self.show_finished)

    def write_stdout(self):
        self.appendPlainText(
                self.process.readAllStandardOutput().data().decode())

    def write_stderr(self):
        self.write_error(self.process.readAllStandardError().data().decode())

    def show_error(self, error):
        if error == self.process.FailedToStart:
            self.write_error("Program cannot be started.\n");
        elif error == self.process.Crashed:
            self.write_error("Program terminated.\n");
        else:
            self.write_error("Error occured during program execution.\n");
        self.process = None

    def write_info(self, text):
        old_format = self.currentCharFormat();
        format = QTextCharFormat()
        format.setForeground(QColor("white"))
        format.setBackground(QColor("darkgreen"))
        self.setCurrentCharFormat(format);
        self.appendPlainText("Done.\n");
        self.setCurrentCharFormat(old_format);

    def show_finished(self, exit_code, exit_status):
        if exit_status == self.process.NormalExit and exit_code == 0:
            self.write_info("Done.")
            self.on_finished.emit(True)
        else:
            self.write_error("The program exited with exit code {0}".format(exit_code));
            self.on_finished.emit(False)
        self.process = None

    def write_error(self, text):
        format = self.currentCharFormat();
        self.setCurrentCharFormat(self.errorformat);
        self.appendPlainText(text);
        self.setCurrentCharFormat(format);
        self.on_finished.emit(False)
        self.process = None
