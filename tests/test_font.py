from fonticon_mdi7 import MDI7
from qtpy.QtWidgets import QPushButton
from superqt.fonticon import icon


def test_MDI7(qtbot):
    btn = QPushButton()
    qtbot.addWidget(btn)
    btn.setIcon(icon(MDI7.sail_boat))
    btn.show()
