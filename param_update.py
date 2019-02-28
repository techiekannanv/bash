'''This script is used to update kernel parameters and modify /etc/sysctl.conf
To update the running kernel this script will use sysctl -w param_name=value
To update the file it will take backup copy, search for the param_name in the
file. If the param_name found with different value then update the value. If
the param_name having same name then don't update. If the param_name not at
all found in the config then add new entry. Whenever the script updating the
config will it will add the ticket/change number before the param_name line.'''

from __future__ import print_function
from datetime import date
from shutil import copy2
import re
import csv

today = date.today().strftime('%m%d%Y')
config = '/home/kannan/sysctl.conf'
sysctl = '/sbin/sysctl'
config_bak = config +'_'+ today
infile = 'infile'

try:
    copy2(config, config_bak)
except:
    print("Error:Unable to make a backup copy of", sysctl)

params = {}

with open(infile) as indata:
    for line in indata:
        if len(line):
            match = re.findall('[\w.]+', line)
            if match:
                params[match[0]] = match[1:]
for param in params.keys():
    print(param,' '.join(params[param]))


