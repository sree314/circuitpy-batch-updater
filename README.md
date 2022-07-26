# CircuitPython firmware batch updater

These small scripts can help update the firmware on
CircuitPython-based boards. They work by connecting to the serial
console and rebooting the board into the UF2 mode. Then, they copy the
updated UF2 bootloader and the updated CircuitPython firmware to the
driver in sequence.

Only tested on Linux. This script is a work in progress.

## Usage

To use this:

```
./batch_update.py /mount/path update-bootloader-itsybitsy_m4-v3.14.0.uf2  adafruit-circuitpython-itsybitsy_m4_express-en_US-7.3.0.uf2
```

Here `/mount/path` refers to the path where the `CIRCUITPY` and the `UF2` drives appear.

## License

Copyright (C) 2022 by Sreepathi Pai

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE

SPDX-License-Identifier: 0BSD
