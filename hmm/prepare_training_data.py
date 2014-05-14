__author__ = 'stefanie'

from count_freqs import *
import re

def calculate_counts(input):
    counts = defaultdict(int)
    iterator = simple_conll_corpus_iterator(input)
    for word, tag in iterator:
        counts[word] += 1
    return counts

def get_rare_class(word):
    if re.match('.*\d+.*', word):
        return "_NUMBER_"
    elif re.match('^[A-Z]+\Z', word):
        return "_CAPITAL_"
    elif re.match('.*[A-Z]\Z', word):
        return "_LAST_CAPITAL_"
    else:
        return "_RARE_"


def replace_rare_word(input, refined_corpusfile):
    counts = calculate_counts(input)
    input.seek(0,0)
    l = input.readline()
    while l:
        line = l.strip()
        if line:  # Nonempty line
            fields = line.split(" ")
            ne_tag = fields[-1]
            word = " ".join(fields[:-1])
            count = counts[word]
            if counts[word] < 5:
                clazz = get_rare_class(word)
                #				print word, clazz
                word = clazz
            refined_corpusfile.write("%s %s\n" % (word, ne_tag))
        else:  # Empty line
            refined_corpusfile.write('\n')
        l = input.readline()


def find_max_tag(counter, word, tags):
    max_tag = ""
    max_count = 0
    for tag in tags:
        count = counter.predict_emssiion_counts[(word, tag)]
        if count > max_count:
            max_tag = tag
            max_count = count
    return max_tag

def calculate_proability(input, counter, counts, output):
    tags = set()
    for ngram in counter.ngram_counts[0]:
        ngramstr = " ".join(ngram)
        tags.add(ngramstr)

    rare_tag = find_max_tag(counter, "_RARE_", tags)
    gene_tag = find_max_tag(counter, "genes", tags)

    l = input.readline()
    while l:
        word = l.strip()
        if word:  # Nonempty line
            max_tag = find_max_tag(counter, word, tags)
            if max_tag:
                output.write("%s %s\n" % (word, max_tag))
            else:
                output.write("%s %s\n" % (word, rare_tag))
        else:
            output.write("\n")
        l = input.readline()

def prepare_train_data():
    input = file(sys.argv[1],"r")
    replace_rare_word(input, sys.stdout)

if __name__ == "__main__":
    prepare_train_data()
