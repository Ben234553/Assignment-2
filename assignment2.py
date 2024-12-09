
#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Biniyam
Semester: Fall 2024 

The python code in this file is original work written by Biniyam. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and violators will be reported and appropriate action will be taken.

Description: This script visualizes memory usage of the system or specific applications using bar charts.
'''

import argparse
import os
import sys

def parse_command_args():
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts", epilog="Copyright 2023")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human readable format")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use if not.")
    return parser.parse_args()

def percent_to_graph(percent: float, length: int = 20) -> str:
    num_hashes = int(percent * length)
    graph = '#' * num_hashes + ' ' * (length - num_hashes)
    return graph

def get_sys_mem() -> int:
    with open('/proc/meminfo', 'r') as file:
        for line in file:
            if 'MemTotal:' in line:
                return int(line.split()[1])
    return 0

def get_avail_mem() -> int:
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

def pids_of_prog(app_name: str) -> list:
    try:
        process = os.popen(f"pidof {app_name}")
        pid_string = process.read().strip()
        process.close()
        return pid_string.split() if pid_string else []
    except Exception as e:
        print(f"Error retrieving PIDs for program {app_name}: {e}")
        return []

def rss_mem_of_pid(proc_id: str) -> int:
    """Returns the RSS memory usage (in KB) for a given PID."""
    rss_mem = 0
    try:
        with open(f'/proc/{proc_id}/smaps', 'r') as smaps:
            for line in smaps:
                if line.startswith("Rss"):
                    rss_mem += int(line.split()[1])
    except FileNotFoundError:
        return 0
    return rss_mem

    

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} {suffixes[suf_count]}'
    return str_result

if __name__ == "__main__":
    args = parse_command_args()

    if args.program:
        pids = pids_of_prog(args.program)
        total_memory_used = sum(rss_mem_of_pid(pid) for pid in pids)
        formatted_memory = bytes_to_human_r(total_memory_used) if args.human_readable else f'{total_memory_used} bytes'
        print(f"Total memory used by {args.program}: {formatted_memory}")
    else:
        total_mem = get_sys_mem()
        avail_mem = get_avail_mem()
        used_mem = total_mem - avail_mem
        mem_usage_percent = used_mem / total_mem
        graph = percent_to_graph(mem_usage_percent, args.length)
        print(f"Memory         [{graph} | {mem_usage_percent*100:.2f}%] {used_mem}/{total_mem}")
