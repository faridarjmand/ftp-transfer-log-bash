#!/bin/bash

# This Script use for Auto Transfer Log with FTP ( Tested in Solaris )

## Created By.Farid Arjmand ##

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

for file in `ls $format`;do
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

for file in `ls $format.gz`;do
        cksum "$file" >> checksum-ftp.txt
done

diff checksum.txt checksum-ftp.txt

if [ "$?" == "0" ];then
        rm $format.gz checksum-ftp.txt checksum.txt listfile.txt listfile-ftp.txt
fi

check

#############################
############ END ############
#############################
