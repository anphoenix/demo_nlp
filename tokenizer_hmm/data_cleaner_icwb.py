# -*- coding: UTF-8 -*-
__author__ = 'stefanie'

import sys

def generate_data(method, training_file, output_file, num, tag_num):
    input = file(training_file, "r")
    output = file(output_file, "w")
    output_answer = file(output_file + ".key", "w")

    count = 0
    for l in input.readlines():
        if num != -1 and count > num:
            break
        line = l.strip()
        if not line:
            print "blank line at no." + str(count)
            continue
        count += 1
        words = line.split("  ")
        for word in words:
            #word is using utf-8 encoding, so default read 4 index in str.
            chars = [word[i:i + 3] for i in range(len(word)) if i % 3 == 0]
            if len(chars) > 0:
                # if len(chars) < 1:
                #     continue
                generate_word(output, chars, True, tag_num)
                if method == "test":
                    generate_word(output_answer, chars, False)
        output.write("\n")
        if method == "test":
            output_answer.write("\n")

def generate_word(output, chars, withTag, tag_num = 2):
    if withTag:
        if tag_num == 4:
            if len(chars) == 1:
                output.write(chars[0] + " " + "S" + "\n")   #S to mark the single word
            else:
                output.write(chars[0] + " " + "B" + "\n")   #B to mark the begining of a long word
                for word in chars[1:-1]:
                    output.write(word + " " + "M" + "\n")    #E to mark the mid of a long word
                output.write(chars[-1] + " " + "E" + "\n")   #E to mark the end of a long word
        else:
            for word in chars[:-1]:
                output.write(word + " " + "B" + "\n")    #B to mark the connected word
            output.write(chars[-1] + " " + "I" + "\n")   #I to mark the end of the word
    else:
        for word in chars:
            output.write(word + "\n")


def Usage():
    print "args: method training_file output_file record_num"
    print "method: training, test"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        Usage()
    else:
        method = sys.argv[1]
        training_file = sys.argv[2]
        output_file = sys.argv[3]
        if len(sys.argv) > 4:
            num = int(sys.argv[4])
        else:
            num = -1;
        if len(sys.argv) > 5:
            tag_num = int(sys.argv[5])
        else:
            tag_num = 2
        generate_data(method, training_file, output_file, num, tag_num)