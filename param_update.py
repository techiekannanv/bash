'''This script is used to update kernel parameters and modify /etc/sysctl.conf
To update the running kernel this script will use sysctl -w param_name=value
To update the file it will take backup copy, search for the param_name in the
file. If the param_name found with different value then update the value. If
the param_name having same name then don't update. If the param_name not at
all found in the config then add new entry. Whenever the script updating the
config will it will add the ticket/change number before the param_name line.'''

from __future__ import print_function
from datetime import date
from shutil import copy2, copymode
import re
from os import system, path


today = date.today().strftime('%m%d%Y')
config = '/etc/sysctl.conf'
sysctl = '/sbin/sysctl'
config_bak = config +'_'+ today
infile = '/tmp/infile'
outfile = '/tmp/params_update.out'

#Take backup copy of the sysctl.conf
try:
    #Check the backup file exists or not
    if path.isfile(config_bak):
        #if exists then increment the copy number
        i=1
        while path.isfile(config_bak+'.'+str(i)):
            i += 1
        config_bak += '.'+str(i)
    copy2(config, config_bak)
except:
    print("Error:Unable to make a backup copy of", config)

def update_kernel(param_value):
    '''This will update kernel parameter with new values in running kernel'''
    command = sysctl +' -w '+ param_value
    system(command)


#Dict to store input parameters and values
params = {}
#Read input file and store params and values in dict params
with open(infile) as indata:
    for line in indata:
        if len(line):
            match = re.findall('[\w.]+', line)
            if match:
                params[match[0]] = match[1:]
                # print(match)

#Open output file to save updated data
with open(outfile, 'w') as outdata:
    #Open config file to process
    with open(config) as data:
        for no,line in enumerate(data):
            #remove new line from every line
            line = line.strip('\n')
            #Check the line is blank or commented
            if re.match(r'\s*\w+', line):
                #Only get param and values
                match = re.findall('[\w.]+', line)
                #Check the current parameter on dict params
                if match[0] in params:
                    #If param name matched and check values are matching or not
                    if match[1:] == params[match[0]]:
                        print("DEBUG: Param {} exists and values matched with sysctl.conf".format(match[0]))
                    else:
                        print("DEBUG: Param {} found and values differ from config and new".format(match[0]))
                        match[1:] = params[match[0]]
                        update_kernel(match[0]+'='+' '.join(match[1:]))
                    #remove the processed param from dict params
                    del(params[match[0]])
                #change the line to updated param = values
                line = match[0] +' = '+ ' '.join(match[1:])
            #Save the commented, blank and processed line in output file
            outdata.write(line +'\n')
            prev_line = line
    #Save new param = values to output file
    if params:
        print("DEBGU: New params adding in end of the file")

        for key, value in params.items():
            outdata.write(key +' = '+ ' '.join(value) +'\n')
            update_kernel(key+'='+' '.join(value))

try:
    copymode(config, outfile)
    copy2(outfile, config)
except:
    print("ERROR: Unable to copy the updated file to config file")

