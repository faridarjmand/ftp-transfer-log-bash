
#!/bin/bash

# This Script use for Auto Transfer Log with FTP ( Tested in Solaris )

## Created By.Farid Arjmand ##
                        ################################# In BASH ##################################

##############################
########## Variable ##########
##############################

host=127.0.0.1
username=testuser
password=testpass
format="*.log"
date=`date +%Y-%m-%d-%H:%M`

red='\033[0;91m'
green='\033[0;92m'
nc='\033[0m'

##############################
############ Main ############
##############################

check ()
{
        if [ "$?" == "0" ];then
                echo -e ${green}"Done"${nc}
        else
                echo -e ${red}"Error !!"${nc}
        fi
}

clear
mkdir $date
numberlog=`ls $format | wc -l | awk ' {print $1} '`
ls -1 $format | awk '{ print length, $0 }' | sort -n | awk '{print $2}' > listfile.txt

for (( i=1; i<=$numberlog; i++ ))
do
        file=`awk 'NR == '$i' {print $1}' listfile.txt`
        report=`du $file |  awk ' {print $1} '`
        if [ "$report" != "0" ];then
                gzip $file
                cksum "$file.gz" >> checksum.txt
        else
                echo -e $file ${red}'Empty!'${nc}
                rm -rf $file
        fi
done

check

##############################
####### FTP Connection #######
##############################

ftp -n -i $host << EOT
ascii
user $username $password
mkdir $date
cd $date
mput $format.gz
put checksum.txt
!mv $format.gz $date/
!cp checksum.txt $date/
mget $format.gz
bye
EOT

check

##############################
####### Data Integrity #######
##############################

numberlog=`ls $format.gz | wc -l | awk ' {print $1} '`
ls -1 $format.gz | awk '{ print length, $0 }' | sort -n | awk '{print $2}' > listfile-ftp.txt

for (( i=1; i<=$numberlog; i++ ))
do
        file=`awk 'NR == '$i' {print $1}' listfile-ftp.txt`
        cksum "$file" >> checksum-ftp.txt
done

diff checksum.txt checksum-ftp.txt

check

if [ "$?" == "0" ];then
        rm $format.gz checksum-ftp.txt checksum.txt listfile.txt listfile-ftp.txt
fi

check

#############################
############ END ############
#############################


                        ################################ In Python #################################

#!/usr/bin/python

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
