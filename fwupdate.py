#!/usr/bin/env python3

from pathlib import Path
import shutil
import os
import serial

class Boot:
    def __init__(self, path):
        self.path = Path(path)
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

    def _do_update(self, src, dst):
        print(f"Updating {dst} from {src}")
        shutil.copyfile(src, dst)
        os.sync()

    def update_bootloader(self, bootfw, update_name = "update-bootloader.uf2"):
        src = bootfw
        dst = self.path / update_name

        self._do_update(src, dst)

    def update_cktpy(self, cktpyfw):
        src = Path(cktpyfw)
        dst = self.path / src.name

        self._do_update(src, dst)

    def eject(self):
        # udiskctl, but need device underlying path
        pass

class CircuitPy:
    def __init__(self, path):
        self.path = Path(path)
        self.boot = None

    def load_boot(self, fname="boot_out.txt"):
        with open(self.path / fname, "r") as f:
            self.boot = [x.strip() for x in f.readlines()]

        return self.boot

    def version(self):
        if self.boot:
            return self.boot[0][:self.boot[0].index(";")]

class Repl:
    def __init__(self, path, cktpy):
        self.path = path
        self.cktpy = cktpy

    def reboot_into_boot(self):
        #if False: # TODO: version check
        #    mode = "microcontroller.RunMode.UF2"
        #else:
        mode = "microcontroller.RunMode.BOOTLOADER"

        # TODO: eject

        x = serial.Serial(self.path, baudrate=115200)
        x.write("\r".encode('utf-8')) # any key to enter REPL
        x.write("import microcontroller\r".encode('utf-8'))
        x.write(f"microcontroller.on_next_reset({mode})\r".encode('utf-8'))
        x.write("microcontroller.reset()\r".encode('utf-8'))

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
    p.add_argument("--bootloader", help="Bootloader update file")
    p.add_argument("--cktpy", help="CircuitPython update")
    p.add_argument("--cpath", default="CIRCUITPY", help="CircuitPy folder basename")
    p.add_argument("--bpath", default="ITSYM4BOOT", help="Boot folder basename")
    p.add_argument("--tty", default="/dev/ttyACM0", help="Path to serial device")

    args = p.parse_args()

    p = scan_path(args.root, args.cpath, args.bpath)

    if p is not None:
        ty, path = p
        if ty == "BOOT":
            b = Boot(path)
            print(b.load_info())
            print(b.uf2_version())
            print("\n".join(b.info))
            if args.bootloader:
                b.update_bootloader(args.bootloader)
            elif args.cktpy:
                b.update_cktpy(args.cktpy)
            else:
                print(f"ERROR: BOOT drive detected, need --bootloader or --cktpy to update firmware")
                sys.exit(1)
        elif ty == "CIRCUITPY":
            cp = CircuitPy(path)
            print(cp.load_boot())
            print(cp.version())
            rp = Repl(args.tty, cp)
            rp.reboot_into_boot()
        else:
            print(f"ERROR: Unrecognized type '{ty}' for path {path}")
    else:
        print(f"ERROR: No CircuitPython partitions detected in {args.root}")


