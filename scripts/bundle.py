import io
import keyword
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple, Union
from zipfile import ZipFile

VERSION = "7.2.96"
PKG_DIR = Path(__file__).parent.parent / "src" / "fonticon_mdi7"
URL = f"https://github.com/Templarian/MaterialDesign-Webfont/archive/refs/tags/v{VERSION}.zip"
CLASSNAME = f"MDI{VERSION[0]}"


def get_data(version: str, pkg_dir: str) -> List[Tuple[Dict[str, str], Path, str]]:
    font_dir = Path(pkg_dir) / "fonts"
    font_dir.mkdir(exist_ok=True)
    ttfs = []

    with urllib.request.urlopen(URL) as response:
        with ZipFile(io.BytesIO(response.read())) as thezip:
            for zipinfo in thezip.infolist():
                if zipinfo.filename.endswith(".ttf") or "LICENSE" in zipinfo.filename:
                    dest = font_dir / Path(zipinfo.filename).name
                    with thezip.open(zipinfo) as source, open(dest, "wb") as target:
                        shutil.copyfileobj(source, target)
                        print("writing", dest)
                    if str(dest).endswith("ttf"):
                        ttfs.append(dest)
                elif zipinfo.filename.endswith("scss/_variables.scss"):
                    with thezip.open(zipinfo) as f:
                        metadata = f.read()
    charmap = {}
    for line in metadata.decode().split("$mdi-icons: (")[1].rstrip(");").splitlines():
        if not line.strip():
            continue
        key, val = line.lstrip("\" '").split('":')
        charmap[key] = chr(int(val.strip(" ,"), 16))

    return [(charmap, ttfs[0], CLASSNAME)]


def _normkey(key: str):
    if key[0].isdigit():
        key = "_" + key
    if keyword.iskeyword(key):
        key += "_"
    key = key.replace("-", "_")
    if not key.isidentifier():
        raise ValueError(f"not identifier: {key}")
    return key


TEMPLATE = """
from pathlib import Path

from ._iconfont import IconFont

FONTS = Path(__file__).parent / "fonts"


class {name}(IconFont):
    '''{doc}.'''
    __font_file__ = str(FONTS / "{file}")
""".strip()


def build(data, version, pkg):
    init = f"__version__ = {version!r}\n\n"
    _all = []

    for charmap, ttf, name in data:
        code = TEMPLATE.format(name=name, doc=ttf.stem, file=ttf.name) + "\n\n"
        for key, glpyh in charmap.items():
            code += f"    {_normkey(key)} = {glpyh!r}\n"

        dest = Path(pkg) / f"{name.lower()}.py"
        dest.write_text(code)
        print("writing", dest)

        init += f"from .{name.lower()} import {name}\n"
        _all.append(name)

    init = f"__all__ = {_all!r}\n" + init
    (Path(pkg) / "__init__.py").write_text(init)
    print("writing __init__.py")


def main(version: str, root: Union[Path, str]):
    build(get_data(version, str(root)), version, root)
    subprocess.run(["pre-commit", "run", "--all-files"])


if __name__ == "__main__":
    main(version=VERSION, root=PKG_DIR)
