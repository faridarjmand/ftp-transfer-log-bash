#!/usr/bin/python

# This Script use for Auto Transfer Log with FTP

## Created By.Farid Arjmand ##

##############################
########## Modules ###########
##############################

import os
import sys
import gzip
import shutil
import hashlib
from ftplib import FTP
from time import strftime

##############################
########## Variable ##########
##############################

host='127.0.0.1'
username='testuser'
password='testpass'

format = ".log"
date = strftime("%Y-%m-%d-%H:%M")

listlog = []

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

def compress(i):
	global j
	j = []
	j.append(str(i))
	j.append('.gz')
	j = ''.join(j)
	infile = open(i, 'rb')
	outfile = gzip.open(j, 'wb')
	outfile.writelines(infile)
	outfile.close()
	infile.close()

def ftp_send(j):
	ftp.storbinary('STOR %s' % j, open(j, 'rb'))
	shutil.move(j, date)

def ftp_recive(jj):
	ftp.cwd('..')
	ftp.retrbinary('RETR %s' % jj,  open(jj, 'wb').write)

def ftp_login(date):
	global ftp
	ftp = FTP(host,username,password)
	ftp.mkd(date)
	ftp.cwd(date)

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

#ftp.storbinary('STOR checksum.txt', open('checksum.txt', 'rb'))
shutil.copy('checksum.txt', date)

ftp.quit()

#############################
############ END ############
#############################
