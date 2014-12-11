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


from base.pointers import make_pointer

from PyQt4.QtGui import QLineEdit, \
                        QFormLayout, \
                        QDoubleValidator, \
                        QGroupBox, \
                        QSpinBox, \
                        QHBoxLayout, \
                        QRegExpValidator, \
                        QComboBox, \
                        QCheckBox
import PyQt4.QtCore as QtCore
import logging

class EditorBase:
    set_text = False


class FloatEditor(EditorBase):

    def make_widget(self, pointer):
        def value_changed(value):
            try:
                f = float(value)
            except ValueError:
                logging.debug("Float editor: Invalid value")
                return
            pointer.set(f)
            #if call_update:
            #    owner.update()
        widget = QLineEdit(str(pointer.get()))
        widget.setValidator(QDoubleValidator())
        widget.textEdited.connect(value_changed)
        return widget


class StringEditor(EditorBase):

    def __init__(self, regex=None, identifier=False):
        if identifier:
            assert not regex
            regex=r'^[A-Za-z_][A-Za-z_\d]*$'
        if regex:
            self.regex = QtCore.QRegExp(regex)
        else:
            self.regex = None

    def make_widget(self, pointer):
        def value_changed(value):
            pointer.set(value)
        widget = QLineEdit(str(pointer.get()))
        if self.regex is not None:
            validator = QRegExpValidator(self.regex)
            widget.setValidator(validator)
        widget.textEdited.connect(value_changed)
        return widget


class IntEditor(EditorBase):

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def make_widget(self, pointer):
        def value_changed(value):
            pointer.set(value)
        widget = QSpinBox()
        widget.setMinimum(self.min_value)
        widget.setMaximum(self.max_value)
        widget.setValue(pointer.get())
        widget.valueChanged.connect(value_changed)
        return widget


class BoolEditor(EditorBase):

    set_text = True

    def __init__(self):
        pass

    def make_widget(self, pointer):
        def value_changed(value):
            pointer.set(value)
        widget = QCheckBox()
        #widget.valueChanged.connect(value_changed)
        return widget


class ChooseEditor(EditorBase):

    def __init__(self, options):
        self.options = options

    def make_widget(self, pointer):
        widget = QComboBox()

        for name, value in self.options:
            widget.addItem(name)

        values = [ value for name, value in self.options ]
        widget.setCurrentIndex(values.index(pointer.get()))

        return widget

class VertexEditor(EditorBase):

    def __init__(self):
        pass

    def make_widget(self, pointer):
        def value_changed():
            try:
                value_x = float(x.text())
                value_y = float(y.text())
                value_z = float(z.text())
            except ValueError:
                logging.debug("Float editor: Invalid value")
                return
            pointer.set((value_x, value_y, value_z))

        vertex = pointer.get()
        layout = QHBoxLayout()

        x = QLineEdit(str(vertex[0]))
        x.setValidator(QDoubleValidator())
        x.textEdited.connect(value_changed)
        layout.addWidget(x)

        y = QLineEdit(str(vertex[1]))
        y.setValidator(QDoubleValidator())
        y.textEdited.connect(value_changed)
        layout.addWidget(y)

        z = QLineEdit(str(vertex[2]))
        z.setValidator(QDoubleValidator())
        z.textEdited.connect(value_changed)
        layout.addWidget(z)

        return layout


class Group:

    def __init__(self, name):
        self.name = name
        self.items = []

    def add(self, editor, name, attr, update_method):
        self.items.append((editor, name, attr, update_method))

    def make_widget(self, owner, layout):
        def add_row(editor, name, attr, update_method):
            if update_method:
                update_callback = lambda: getattr(owner, update_method)()
            else:
                update_callback = None
            pointer = make_pointer(owner, attr, update_callback)
            widget = editor.make_widget(pointer)
            if editor.set_text:
                widget.setText(name)
                form_layout.addRow(widget)
            else:
                form_layout.addRow(name, widget)

        form_layout = QFormLayout()
        box = QGroupBox(self.name);
        layout.addWidget(box)
        box.setLayout(form_layout)

        for editor, name, attr, update_method in self.items:
            add_row(editor, name, attr, update_method)

    def add_float(self, name, attr, update_method="update"):
        self.add(FloatEditor(), name, attr, update_method)

    def add_int(self, name, attr, update_method="update", *args, **kw):
        self.add(IntEditor(*args, **kw), name, attr, update_method)

    def add_bool(self, name, attr, update_method="update", *args, **kw):
        self.add(BoolEditor(*args, **kw), name, attr, update_method)

    def add_vertex(self, name, attr, update_method="update", *args, **kw):
        self.add(VertexEditor(*args, **kw), name, attr, update_method)

    def add_string(self, name, attr, update_method="update", *args, **kw):
        self.add(StringEditor(*args, **kw), name, attr, update_method)

    def add_choose(self, name, attr, update_method="update", *args, **kw):
        self.add(ChooseEditor(*args, **kw), name, attr, update_method)


class EditorBuilder:

    def __init__(self):
        self.groups = []

    def add_group(self, name):
        group = Group(name)
        self.groups.append(group)
        return group
        """
        last = self.groups[-1]
        if last.name is None and not last.items:
            # Last group is empty default group, so we can remove it
            self.groups = [ Group ]
        else:
            self.groups.append(group)
        """

    def build(self, owner, layout):
        for group in self.groups:
            group.make_widget(owner, layout)
