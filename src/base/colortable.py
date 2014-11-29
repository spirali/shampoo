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


from PyQt4.QtGui import QColor


color_table = [
    QColor("#a6ff00"), QColor("#f20000"), QColor("#0066ff"), QColor("#ff0099"),
    QColor("#8c0000"), QColor("#080099"), QColor("#265499"), QColor("#b3d96c"),
    QColor("#80b3ff"), QColor("#4d8040"), QColor("#ff0000"), QColor("#00ffb2"),
    QColor("#0d00ff"), QColor("#00778c"), QColor("#910099"), QColor("#00bf30"),
    QColor("#ff405c"), QColor("#bf80ff"), QColor("#ffb980"), QColor("#563973"),
    QColor("#ffe600"), QColor("#00d9ff"), QColor("#f200ff"), QColor("#8c3f00"),
    QColor("#ff7300"), QColor("#998a00"), QColor("#59b398"), QColor("#a65353"),
    QColor("#b3598f")
]


def colors_gen():
    i = 0
    while True:
        yield color_table[i]
        i = (i + 1) % len(color_table)
