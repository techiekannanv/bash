#!/bin/bash
#This script is used to give current CPU load
#This will be calculate from load average from uptime command
#less than or equal to 30% --> Show in Green
#less than or equal to 70% --> Show in Yellow
#greater than 70% --> Show in error
no_of_cpus=`grep -c processor /proc/cpuinfo`
uptime |awk -F"," -v cpus=$no_of_cpus -v highlight="\033[7m" '{sub(".*: ","",$(NF-2));load=$(NF-2);
cpu=(load/cpus)*100;
if(cpu<=30){
	color="\033[32m"
}
else if(cpu>30 && cpu<=70){
	color="\033[33m"
}
else{
	color="\033[31m"
}
}
END{
printf("%sCPU: %s%.f%\033[0m",highlight,color,cpu);
}'
