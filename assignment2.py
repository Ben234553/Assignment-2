#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "Student Name"
Semester: "Enter Winter/Summer/Fall Year"

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script visualizes memory usage of the system or specific applications using bar charts.
'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int = 20) -> str:
    num_hashes = int(percent * length)
    graph = '#' * num_hashes + ' ' * (length - num_hashes)
    return graph

def get_sys_mem() -> int:
    """ Returns the total system memory in kB """
    with open('/proc/meminfo', 'r') as file:
        for line in file:
            if 'MemTotal:' in line:
                return int(line.split()[1])
    return 0

def get_avail_mem() -> int:
    """ Returns the available system memory in kB """
    mem_free = 0
    swap_free = 0
    with open('/proc/meminfo', 'r') as file:
        for line in file:
            if 'MemAvailable:' in line:
                return int(line.split()[1])
            elif 'MemFree:' in line:
                mem_free = int(line.split()[1])
            elif 'SwapFree:' in line:
                swap_free = int(line.split()[1])
    return mem_free + swap_free

if __name__ == "__main__":
    args = parse_command_args()

    # Retrieve memory statistics
    total_mem = get_sys_mem()
    avail_mem = get_avail_mem()
    used_mem = total_mem - avail_mem

    # Calculate the percentage of used memory
    mem_usage_percent = used_mem / total_mem

    # Generate a graphical representation of memory usage
    graph = percent_to_graph(mem_usage_percent, args.length)

    print("Memory Usage Graph:")
    print(graph)


def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        ...
    else:
        ...
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
