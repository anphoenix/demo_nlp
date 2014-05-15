# -*- coding: UTF-8 -*-
__author__ = 'stefanie'

import sys

def generate_training(input, output, num):
    count = 0
    for l in input.readlines():
        if count > num:
            break
        line = l.strip()
        if not line:
            print count
            continue
        count += 1
        #“  这  首先  是  个  民族  问题  ，  民族  的  感情  问题  。
        fields = line.split("  ")
        for field in fields:
            words = [field[i:i + 3] for i in range(len(field)) if i % 3 == 0]
            if len(words) < 1:
                continue
            for word in words[:-1]:
                output.write(word + " " + "B" + "\n")
            output.write(words[-1] + " " + "I" + "\n")
        output.write("\n")

def generate_test(input, output_key, output_val, num):
    l = input.readline()
    count = 0
    print num
    for l in input.readlines():
        line = l.strip()
        if not line:
            break
        count += 1
        #“  这  首先  是  个  民族  问题  ，  民族  的  感情  问题  。
        #print count
        if count > num:
            break

        fields = line.split("  ")
        for field in fields:
            words = [field[i:i + 3] for i in range(len(field)) if i % 3 == 0]
            if len(words) < 1:
                continue
            for word in words[:-1]:
                output_key.write(word + "\n")
                output_val.write(word + " " + "B" + "\n")
            output_key.write(words[-1] + "\n")
            output_val.write(words[-1] + " " + "I" + "\n")
        output_key.write("\n")
        output_val.write("\n")
        #l = input.readline()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        print "args: method training_file output_file num"
        print "method: training, test"
        method = "test"
    if len(sys.argv) > 2:
        training_file = sys.argv[2]
    else:
        training_file = "/opt/data/nlp/icwb2-data/training/msr_training.utf8"
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    else:
        output_file = "output"
    if len(sys.argv) > 4:
        num = int(sys.argv[4])
    else:
        num = 1000
    input = file(training_file,"r")
    print method
    if method == "training":
        print "generate training data"
        output = file(output_file,"w")
        generate_training(input, output, num)
    elif method == "test":
        print "generate test data"
        output_key = file(output_file+".key","w")
        output_val = file(output_file+".val", "w")
        generate_test(input, output_key, output_val, num)
