__author__ = 'stefanie'

import sys

def format_result(input):
    sents = ""
    for l in input.readlines():
        line = l.strip()
        if not line:
            print sents
            sents = ""
        else:
            fields = line.split(" ")
            if len(fields) >= 2:
                if fields[1] == 'I':
                    sents += fields[0] + " "
                else:
                    sents += fields[0]

if __name__ == "__main__":
    input_file = file(sys.argv[1],"r")
    format_result(input_file)
