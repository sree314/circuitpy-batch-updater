#!/usr/bin/env python3

from pathlib import Path
import shutil
import os

class Boot:
    def __init__(self, path):
        self.path = path
        self.header = None
        self.info = None

    def load_info(self, fname = "INFO_UF2.TXT"):
        f = self.path / "INFO_UF2.TXT"
        with open(f, "r") as info:
            self.info = [x.strip() for x in info.readlines()]
            self.header = self.info[0]

        return self.info

    def uf2_version(self, prefix = "UF2 Bootloader"):
        if self.header and self.header.startswith(prefix):
            return self.header[len(prefix)+2:]

        return None

    def update_fw(self, bootfw, update_name = "update-bootloader.uf2"):
        src = bootfw
        dst = self.path / update_name

        print(src, dst)
        #shutil.copyfile(src, dst)
        #os.sync()

def scan_path(root, cpyname = "CIRCUITPY", bootname = "BOOT"):
    root = Path(root)

    for ty, p in [("CIRCUITPY", cpyname), ("BOOT", bootname)]:
        d = (root / p)
        if d.exists() and d.is_dir():
            return ty, d

    return None

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Update firmware on a CircuitPy device")

    p.add_argument("root", help="Root under which the CIRCUITPY and BOOT drives are automounted")
    p.add_argument("--bootloader", help="Bootloader file")
    p.add_argument("--cpath", default="CIRCUITPY", help="CircuitPy folder basename")
    p.add_argument("--bpath", default="ITSYM4BOOT", help="Boot folder basename")

    args = p.parse_args()

    p = scan_path(args.root, args.cpath, args.bpath)

    if p is not None:
        ty, path = p
        if ty == "BOOT":
            b = Boot(path)
            print(b.load_info())
            print(b.uf2_version())
            print("\n".join(b.info))
            assert args.bootloader is not None, "Need bootloader file to update"
            b.update_fw(args.bootloader)
        elif ty == "CIRCUITPY":
            pass
        else:
            print(f"ERROR: Unrecognized type '{ty}' for path {path}")
    else:
        print(f"ERROR: No CircuitPython partitions detected in {args.root}")


