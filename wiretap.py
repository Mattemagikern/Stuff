#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from termcolor import colored
import serial
import time
import sys
import glob
import os
from threading import Thread

li = []
def read_uart(s):
    while s.isOpen():
        try:
            line = s.readline()[:-1]
            if len(line) > 0:
                if any(word in line for word in keywords):
                    line = colored(line, "yellow", attrs=["bold", "underline"])
                elif "/E" in line:
                    line = colored(line, "red", attrs=["bold", "underline"])
                elif "/D" in line:
                    line = colored(line, "light_gray")
                elif "/I" in line:
                    line = colored(line, "cyan")
                else:
                    line = colored(line, "white")

                print line
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
            print
        except:
            raise

def send_input(s):
    while s.isOpen():
        try:
            read = sys.stdin.readline();
            if read[0] == "#" and len(read) == 2:
                print "previous commands"
                for i,o in enumerate(li):
                    print i, o
            elif read[0] == "#":
                print li[int(read[1:-1])]
                s.write(li[int(read[1:-1])])
            else:
                print read,
                s.write(read)
                li = [read] + li[:9]
        except (KeyboardInterrupt, SystemExit):
            print
            sys.exit(0)
        except:
            raise 

if __name__ == "__main__":
    keywords = sys.argv[1:]
    ports = ["\\.\COM%s" % (i + 1) for i in range(10)]
    ports += glob.glob("/dev/tty[A-Za-z]*")
    s = None
    for port in ports:
        try:
            s = serial.Serial(port, 115200, timeout = 2,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE)
            break
        except Exception as _:
            pass
    if s:
        os.system('clear')
        t1 = Thread(target = read_uart, args = (s,)).start()
        t2 = Thread(target = send_input, args = (s,)).start()
        t1.daemon = True
        t2.daemon = True
        try:
            while True:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print
            sys.exit(0)
        except:
            raise
    else:
        print colored("Did not find an open port :(", "red")
