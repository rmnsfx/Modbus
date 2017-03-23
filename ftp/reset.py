#!/usr/bin/python
# coding: utf-8

from usb.core import find as finddev


if __name__ == "__main__":		

			dev = finddev(idVendor=0x12d1)
			dev.reset()	