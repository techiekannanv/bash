#!/usr/bin/python

from __future__ import print_function
import lookup
import pingip
import argparse
import multiprocessing as mp
import time
import logging
from prettytable import PrettyTable


output = mp.Queue()
limits = 5

def worker(ip,count, timeout):
    resolve = list(lookup.Lookup(ip))
    print(' : '.join(resolve) +' : '+ pingip.Ping(resolve[0], count, timeout))
#    resolve.append(pingip.Ping(resolve[0], count, timeout))
#    output.put(resolve)

parse = argparse.ArgumentParser(description='This script is used to ping multiple ips in parallel')
parse.add_argument('-f', action='store', dest='file', default=None)
parse.add_argument('-i', action='store', dest='ip', default=None)
parse.add_argument('-c', action='store', dest='count', default=3)
parse.add_argument('-W', action='store', dest='timeout', default=1)
parse.add_argument('-fmt', action='store', dest='format', default='line')
args = parse.parse_args()
ips = []
#mp.log_to_stderr(logging.INFO)
if ( args.file == None and args.ip == None ):
    parse.print_help()

if ( args.file != None ):
    with open(args.file,'r') as file:
        for line in file:
            ips.append(line.strip())

if (args.ip != None):
    ips.append(args.ip)
procs = []
while ( ips ):
    if ( len(mp.active_children()) < limits ):
        proc = mp.Process(target=worker, args=(ips.pop(),args.count, args.timeout))
        procs.append(proc)
        proc.start()

for proc in procs:
    if proc.is_alive():
        proc.join()
#final = []
#while not output.empty():
#    final.append(output.get())
#
#if args.format == 'line':
#    for entry in final:
#        print(' : '.join(entry))
#elif args.format == 'table':
#    table = PrettyTable()
#    table.field_names = ['IP Address', 'HostName', 'Status']
#    for entry in final:
#        table.add_row(entry)
#    table.sortby='Status'
#    print(table)
