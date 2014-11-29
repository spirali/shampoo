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


from base.geom import BoundingBox
from ui.console import Console
from ui.glwidget import GLWidget
import ui.qtutils

from PyQt4.QtGui import QMainWindow, \
                        QPushButton, \
                        QSizePolicy, \
                        QSpacerItem, \
                        QSplitter, \
                        QTabWidget, \
                        QTreeView, \
                        QHBoxLayout, \
                        QVBoxLayout, \
                        QWidget


class MainWindow(QMainWindow):

    def __init__(self, shampoo):
        super().__init__()
        self.setWindowTitle("Shampoo")
        self.resize(800, 400)
        #self.showMaximized()
        self.shampoo = shampoo
        self._create_central_widget()
        self._create_main_menu()

        self.case = None
        self.tree = None

    def set_case(self, case):
        self.case = case

        self.case.rebuild_scene.connect(self.rebuild_scene)

        self.tree = case.make_tree(self)
        self.tree.rebuild_scene.connect(self.rebuild_scene)
        self.treeview.setModel(self.tree)
        self.treeview.expandAll()
        self.treeview.selectionModel().currentChanged.connect(self._select_node)
        self.rebuild_scene()
        self.focus_on_node(self.tree)
        self.update_title()

    def select_node(self, node):
        layout = self.editwidget.layout()
        ui.qtutils.clean_layout(layout)
        node.make_editor(layout)
        layout.addSpacerItem(
                QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

    def focus_on_node(self, node):
        items = []
        node.collect_render_items(items)
        bounding_box = BoundingBox()
        for item in items:
            bounding_box.add_box(item.bounding_box)
        if bounding_box.is_valid():
            self.glwidget.focus_on_bounding_box(bounding_box)

    def rebuild_scene(self):
        items = []
        self.tree.collect_render_items(items)
        self.glwidget.render_items = items
        self.glwidget.update()

    def update_title(self):
        if not self.case or not self.case.path:
            self.setWindowTitle("Shampoo")
        else:
            self.setWindowTitle("Shampoo - " + self.case.path)

    def _select_node(self, current, old):
        node = current.internalPointer()
        if node is None:
            return
        self.select_node(node)

    def _create_main_menu(self):
        menu = self.menuBar().addMenu("&Case")
        a = menu.addAction("&New")

        a = menu.addAction("&Open")
        a.triggered.connect(self.shampoo.open)

        a = menu.addAction("&Save")
        a.triggered.connect(self.shampoo.save)

        a = menu.addAction("Save &as")
        a.triggered.connect(self.shampoo.save_as)

        menu.addSeparator()
        a = menu.addAction("&Quit")
        a.triggered.connect(self.shampoo.app.quit)

    def _create_central_widget(self):

        tabs = QTabWidget()

        splitter = QSplitter()
        self.treeview = QTreeView()
        self.treeview.header().hide()
        self.treeview.resize(500, 0)
        splitter.addWidget(self.treeview)

        self.editwidget = QWidget()
        self.editwidget.setLayout(QVBoxLayout())
        self.editwidget.resize(300, 300)
        self.editwidget.setMinimumSize(300, 100)
        splitter.addWidget(self.editwidget)

        self.glwidget = GLWidget()
        splitter.addWidget(self.glwidget)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 4)

        tabs.addTab(splitter, "Mesh")

        tabs.addTab(self._create_run(), "Run")

        self.setCentralWidget(tabs)

    def _create_run(self):
        run = QSplitter()

        buttons = QWidget()
        layout = QVBoxLayout()
        buttons.setLayout(layout)

        button = QPushButton("Make Basemesh")
        button.clicked.connect(self.shampoo.run)
        layout.addWidget(button)

        button_terminate = QPushButton("Terminate")
        button_terminate.clicked.connect(self.shampoo.run)
        button_terminate.setEnabled(False)
        layout.addWidget(button_terminate)

        layout.addSpacerItem(
                QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        run.addWidget(buttons)

        self.console = Console()
        run.addWidget(self.console)
        return run
