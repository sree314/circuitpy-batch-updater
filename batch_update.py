#!/usr/bin/env python3

import argparse
from fwupdate import *
import sys
import time

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Update firmware on CircuitPy devices")

    p.add_argument("root", help="Root under which the CIRCUITPY and BOOT drives are automounted")
    p.add_argument("bootloader", help="Bootloader update file")
    p.add_argument("cktpy", help="CircuitPython update")
    p.add_argument("--cpath", default="CIRCUITPY", help="CircuitPy folder basename")
    p.add_argument("--bpath", default="ITSYM4BOOT", help="Boot folder basename")
    p.add_argument("--tty", default="/dev/ttyACM0", help="Path to serial device")

    args = p.parse_args()

    if p is None:
        print(f"ERROR: No CircuitPython partitions detected in {args.root}")
        sys.exit(1)

    bootloader_updated = False
    cktpy_updated = False

    p = scan_path(args.root, args.cpath, args.bpath)
    ty, p = p

    if ty == "CIRCUITPY":
        cp = CircuitPy(p)
        cp.load_boot()
        print(cp.boot[0])

        rp = Repl(args.tty, cp)
        rp.reboot_into_boot()
        time.sleep(5)

        p = scan_path(args.root, args.cpath, args.bpath)
        if p is None:
            print(f"ERROR: No CircuitPython partitions detected in {args.root} after reboot")
            sys.exit(1)

        ty, p = p

    if ty == "BOOT":
        cp = Boot(p)
        cp.load_info()
        print(cp.uf2_version())
        print("Updating Bootloader")
        cp.update_bootloader(args.bootloader)

        while True:
            print(f"Waiting for {p}")
            time.sleep(5)
            if p.exists(): break

        print("Updating CircuitPython")
        cp.update_cktpy(args.cktpy)

        p = p.parent / args.cpath
        while True:
            print(f"Waiting for {p}")
            time.sleep(5)
            if p.exists(): break

    print("Done")
