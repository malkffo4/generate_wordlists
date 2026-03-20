#!/usr/bin/env python

'''
Combine password list for bypass broken autentification.
This works if the backend allows us to log in when we pass it a list of passwords.
'''
import sys

if len(sys.argv) != 5:
    print("Usage: python add_password.py <PREFIX> <POSTFIX> <when to repeat> <file name>")
    sys.exit(1)

PREFIX   = sys.argv[1]
POSTFIX  = sys.argv[2]
try:
    REPEAT   = int(sys.argv[3])
except Exception as err:
    print(err)
    exit(1)

filename = sys.argv[4]
lines = []

try:
    with open(filename, 'r') as f:
        lines = f.readlines()

    if lines[-1].strip() == '':
        lines.pop()  
except FileNotFoundError:
    print(f"File '{filename}' not found.")

list_pass = PREFIX

for line in lines.copy():
    line = line.strip('\n')
    list_pass = list_pass + f'"{line}",'

list_pass = list_pass[:-1] + POSTFIX

for i, line in enumerate(lines.copy()):
    line = line.strip('\n')
    print(f'"{line}"')
    if (i % REPEAT) == 0:
        print(list_pass)
