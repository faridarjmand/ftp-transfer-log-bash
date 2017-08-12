#!/bin/bash

# This Script use for Transfer File witch FTP

##############################
########## Variable ##########
##############################

host=127.0.0.1
username=testuser
password=testpass
format="*.log"
datee=`date +%Y-%m-%d-%H:%M`

red='\033[0;31m'
green='\033[0;32m'
nc='\033[0m'

##############################
############ Main ############
##############################

check ()
{
        if [ "$?" == "0" ];then
                echo -e ${green}"Done"${nc}
        else
                echo -e ${red}"Error"${nc}
        fi
}

clear
mkdir $datee
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
                sleep 2
        fi
done

check

##############################
####### FTP Connection #######
##############################

ftp -n -i $host << EOT
ascii
user $username $password
mkdir $datee
cd $datee
mput $format.gz
put checksum.txt
!mv $format.gz $datee/
!cp checksum.txt $datee/
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
