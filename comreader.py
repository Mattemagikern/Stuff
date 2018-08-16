from termcolor import colored
import serial
import time
import sys
import glob
import os

keywords = sys.argv[1:]
ports = ["\\.\COM%s" % (i + 1) for i in range(10)]
ports += glob.glob("/dev/tty[A-Za-z]*")
for port in ports:
    try:
        s = serial.Serial(port, 115200, timeout = 2,
                bytesize = serial.EIGHTBITS,
                parity = serial.PARITY_NONE)
        break
    except Exception as _:
        pass

os.system('clear')
while s.isOpen():
    try:
        line = s.readline()[:-1]
        if len(line) > 0:
            if any(word in line for word in keywords):
                line = colored(line, "yellow", attrs=["bold"])
            elif "ERROR:" in line:
                line = colored(line, "red", attrs=["bold"])
            elif "/D" in line:
                line = colored(line, "white")
            elif "/I" in line:
                line = colored(line, "cyan")
            else:
                line = colored(line, "grey")

            print line
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
    except:
        raise
