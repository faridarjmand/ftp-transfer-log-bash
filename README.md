## Created By.Farid Arjmand ##

### This Script use for Auto Transfer Log with FTP


In BASH & Python


```sh
#!/bin/bash
# This Script use for Auto Transfer Log with FTP ( Tested in Solaris )
## Created By.Farid Arjmand ##
######################################## Variable ########################################
host=127.0.0.1username=testuserpassword=testpassformat="*.log"date=`date +%Y-%m-%d-%H:%M`
red='\033[0;91m'green='\033[0;92m'nc='\033[0m'
########################################## Main ##########################################
check (){        if [ "$?" == "0" ];then                echo -e ${green}"Done"${nc}        else                echo -e ${red}"Error !!"${nc}        fi}
clearmkdir $datenumberlog=`ls $format | wc -l | awk ' {print $1} '`ls -1 $format | awk '{ print length, $0 }' | sort -n | awk '{print $2}' > listfile.txt
for (( i=1; i<=$numberlog; i++ ))do        file=`awk 'NR == '$i' {print $1}' listfile.txt`        report=`du $file |  awk ' {print $1} '`        if [ "$report" != "0" ];then                gzip $file                cksum "$file.gz" >> checksum.txt        else                echo -e $file ${red}'Empty!'${nc}                rm -rf $file        fidone
check
##################################### FTP Connection #####################################
ftp -n -i $host << EOTasciiuser $username $passwordmkdir $datecd $datemput $format.gzput checksum.txt!mv $format.gz $date/!cp checksum.txt $date/mget $format.gzbyeEOT
check
##################################### Data Integrity #####################################
numberlog=`ls $format.gz | wc -l | awk ' {print $1} '`ls -1 $format.gz | awk '{ print length, $0 }' | sort -n | awk '{print $2}' > listfile-ftp.txt
for (( i=1; i<=$numberlog; i++ ))do        file=`awk 'NR == '$i' {print $1}' listfile-ftp.txt`        cksum "$file" >> checksum-ftp.txtdone
diff checksum.txt checksum-ftp.txt
check
if [ "$?" == "0" ];then        rm $format.gz checksum-ftp.txt checksum.txt listfile.txt listfile-ftp.txtfi
check
######################################### END #########################################
```
