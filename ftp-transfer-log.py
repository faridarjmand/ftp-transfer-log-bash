#!/usr/bin/python

# This Script use for Auto Transfer Log with FTP

## Created By.Farid Arjmand ##

import os
import sys
import gzip
import socket
import shutil
import hashlib
import difflib
from ftplib import FTP
from time import strftime

##############################
########## Variable ##########
##############################

host='172.16.1.151'
username='test'
password='!QAZ2wsx3edc'

format = ".log"
date = strftime("%Y-%m-%d-%H:%M")

listlog = []
ftplist = []

###############################
########## Functions ##########
###############################

def checksum(j):
	temp = sys.stdout
	sys.stdout = open('checksum.txt', 'a')
	hash = hashlib.md5(open(j, 'rb').read()).hexdigest()
	print(j, hash)
	sys.stdout.close()
	sys.stdout = temp

def checksum_ftp(ii):
	temp = sys.stdout
	sys.stdout = open('checksum_ftp.txt', 'a')
	hash = hashlib.md5(open(ii, 'rb').read()).hexdigest()
	print(ii, hash)
	sys.stdout.close()
	sys.stdout = temp
	os.remove(ii)

def compress(i):
	global j
	j = []
	j.append(str(i))
	j.append('.gz')
	j = ''.join(j)
	ftplist.append(j)
	infile = open(i, 'rb')
	outfile = gzip.open(j, 'wb')
	outfile.writelines(infile)
	outfile.close()
	infile.close()

def ftp_send(j):
	ftp.storbinary('STOR %s' % j, open(j, 'rb'))
	shutil.move(j, date)

def ftp_recive(ii):
	ftp.retrbinary('RETR %s' % ii,  open(ii, 'wb').write)

def ftp_login(date):
	global ftp
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((host, 21))
	if result == 0:
		ftp = FTP(host,username,password)
		ftp.mkd(date)
		ftp.cwd(date)
	else:
		print("Can't Connect To Server")
		exit()

def remove_checksum():
	for check in os.listdir("."):
		if check.startswith("checksum"):
			os.remove(check)

def diff_checksum():
	diff = difflib.ndiff(open('checksum.txt').readlines(), open('checksum_ftp.txt').readlines())
	try:
		while 1:
			print diff.next(),
	except:
		pass

##############################
############ Main ############
##############################

for log in os.listdir("."):
	if log.endswith(format):
		listlog.append(os.path.join(log))

os.system("clear")
os.makedirs(date)
ftp_login(date)

for i in listlog:
	if os.path.isfile(i):
		size = os.stat(i).st_size
		if size != 0:
			compress(i)
			checksum(j)
			ftp_send(j)
		os.remove(i)

ftp.storbinary('STOR checksum.txt', open('checksum.txt', 'rb'))
shutil.copy('checksum.txt', date)

for ii in ftplist:
	ftp_recive(ii)
	checksum_ftp(ii)

ftp.quit()
diff_checksum()
remove_checksum()

##############################
############ END #############
##############################
