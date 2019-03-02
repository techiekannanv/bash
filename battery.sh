#!/bin/bash
#Show battery status like(charging/discharging, percentage of battery, hours remaining)
#This script require acpi tool need to install on the system
#Charging --> ^
#Discharging --> v
#71-100% --> Show in green
#31-70% --> Show in yellow
#Bellow or equal to 30% --> Show in Red

which acpi >/dev/null 2>&1 
if [ $? -ne 0 ]
then
	echo  "Error:acpi tool is not installed on this system." 
       	exit 2 
else
	#Is battery charging or discharging?
	acpi -b |grep -q -w Charging && charging="^" || charging="v"
	percentage=`acpi -b |awk -F"," '{sub("%","",$2);$2=$2*1;
	if($2>70){color="\033[32m";}
	else if($2>30 && $2<70 ){color="\033[33m";}
	else if($2<30){color="\033[31m";}}
	END{printf("%s%d%",color,$2);}'`
	remain_hours=`acpi -b|awk -F"," '{sub("[a-zA-Z]+.*","",$NF);printf("%s",$NF);}'`
	echo -en "\033[7mBattery: $percentage-$charging-$remain_hours\033[0m"
fi
