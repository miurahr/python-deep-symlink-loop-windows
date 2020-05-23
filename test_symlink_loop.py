import os
import pathlib

import pytest


def walk(path, dereference=True):
    if path.is_symlink() and not dereference:
        print(path)
    elif path.is_file():
        print(path)
    elif path.is_dir():
        if not path.samefile('.'):
            print(path)
        for nm in sorted(os.listdir(str(path))):
            walk(path.joinpath(nm))



def test_symlink_deep_loop(tmp_path):
    origin = tmp_path / 'src' / 'original.txt'
    origin.parent.mkdir(parents=True, exist_ok=True)
    with origin.open('w') as f:
        f.write("Original")
    slink = tmp_path / "src" / "link"
    slink.parent.mkdir(parents=True, exist_ok=True)
    target = pathlib.Path('../parent/original.txt')
    slink.symlink_to(target, False)
    plink = tmp_path / "src" / "parent"
    plink.symlink_to(tmp_path / "src", False)
    walk(tmp_path / 'src')
