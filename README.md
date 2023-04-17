# fonticon-materialdesignicons7

[![License](https://img.shields.io/pypi/l/fonticon-materialdesignicons7.svg?color=green)](https://github.com/pyapp-kit/fonticon-materialdesignicons7/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/fonticon-materialdesignicons7.svg?color=green)](https://pypi.org/project/fonticon-materialdesignicons7)
[![Python Version](https://img.shields.io/pypi/pyversions/fonticon-materialdesignicons7.svg?color=green)](https://python.org)

[Material Design Icons 7](https://github.com/Templarian/MaterialDesign-Webfont) extension for [superqt font icons](https://pyapp-kit.github.io/superqt/utilities/fonticon/)

<https://github.com/templarian/MaterialDesign>

```sh
pip install superqt fonticon-materialdesignicons7
```

```python
from fonticon_mdi7 import MDI7
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QApplication, QPushButton
from superqt.fonticon import icon, pulse

app = QApplication([])

btn2 = QPushButton()
btn2.setIcon(icon(MDI7.fan, animation=pulse(btn2)))
btn2.setIconSize(QSize(225, 225))
btn2.show()

app.exec_()
```

### Dev note

To update this package for new fonticon releases, update the `VERSION = ...` string
in `scripts/bundle.py`, and rerun `python scripts/bundle.py`.
