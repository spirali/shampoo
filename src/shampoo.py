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

from foam.case import Case

from PyQt4.QtCore import QProcess
from PyQt4.QtGui import QApplication, QFileDialog
from ui.mainwindow import MainWindow
import argparse
import logging
import sys


class Shampoo:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow(self)

        args = self._parse_args()

        if args.level == 0:
            level = logging.ERROR
        elif args.level == 1:
            level = logging.INFO
        else:
            level = logging.DEBUG

        logging.basicConfig(format="%(levelname)s: %(message)s", level=level)

        self.case = Case()
        if args.load:
            self.case.load(args.load)
        self.window.set_case(self.case)

    def open(self):
        dirname = QFileDialog.getExistingDirectory(
            self.window, "Load OpenFOAM case", ".")
        if not dirname:
            return
        self.case = Case()
        self.case.load(dirname)
        self.window.set_case(self.case)

    def save(self):
        self.case.path = "/home/spirali/tmp/svtest"
        if self.case.path:
            self.case.save()
        else:
            self.save_as()

    def save_as(self):
        dirname = QFileDialog.getSaveFileName(
            self.window, "Save OpenFOAM case", ".")
        if not dirname:
            return
        self.case.path = dirname
        self.case.save()
        self.window.update_title()

    def main(self):
        self.window.show()
        return self.app.exec_()

    def _parse_args(self):
        parser = argparse.ArgumentParser(
            description="Shampoo -- OpenFoam configuration tool")
        parser.add_argument("--load",
                            metavar="DIRECTORY",
                            type=str,
                            help="Load OpenFoam case")
        parser.add_argument("--level",
                            metavar="LEVEL",
                            type=int,
                            default=1,
                            help="Verbose level, default: 1")
        return parser.parse_args()

    def run(self):
        program_name = "/bin/ls"
        logging.info("Running %s", program_name)
        process = QProcess()
        process.start(program_name)
        self.window.console.set_process(process)


if __name__ == "__main__":
    sys.exit(Shampoo().main())
