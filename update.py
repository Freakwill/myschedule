# -*- coding: utf-8 -*-
"""Python script for myschedule"""

import argparse
import script


parser = argparse.ArgumentParser(description='Update desk.')
parser.add_argument('-o', dest='output', action='store', metavar='STRING', help='the current output')
parser.add_argument('-d', dest='domEl', action='store', metavar='STRING', help='DOM Elements')

args = parser.parse_args()

output = args.output
domEl = args.domEl

todolist = script.todolist
print(todolist.report())