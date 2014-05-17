# -*- coding: UTF-8 -*-
__author__ = 'stefanie'

import sys

def format_result(input):
    sents = ""
    for l in input.readlines():
        line = l.strip()
        if not line:
            if sents:
                print sents
                sents = ""
        else:
            fields = line.split(" ")
            if len(fields) >= 2:
                if fields[1] in 'SEI':
                    sents += fields[0] + "  "
                else:
                    sents += fields[0]
def Usage():
    print "python result_formatter.py raw_result > formatted result"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        Usage()
    else:
        input_file = file(sys.argv[1], "r")
        format_result(input_file)
