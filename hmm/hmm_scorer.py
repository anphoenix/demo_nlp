#! /usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "Stefanie Zhao <zhaochenting@gmail.com>"
__date__ = "$Mar 11, 2013"

from hmm_trainer import *
import re

def is_rare_word(counter, word, tags):
    for tag in tags:
        count = counter.predict_emssiion_counts[(word, tag)]
        if count > 0:
            return False
    return True

def get_possible_tags(index, tags, begin):
    if index > 0:
        return tags
    else:
        return begin

def get_rare_class(word):
    if re.match('.*\d+.*', word):
        return "_NUMBER_"
    elif re.match('^[A-Z]+\Z', word):
        return "_CAPITAL_"
    elif re.match('.*[A-Z]\Z', word):
        return "_LAST_CAPITAL_"
    else:
        return "_RARE_"

def viterbi(counter, input, output):
	sents = sentence_iterator(simple_conll_corpus_iterator(input))
	tags = set()
	for ngram in counter.ngram_counts[0]:
		ngramstr = " ".join(ngram)
		tags.add(ngramstr)
		
	begin = set()
	begin.add("*")
		
	for sent in sents:
		# print sent
		pi = defaultdict(float)
		pi_tag = defaultdict(str)
		pi[(0, "*", "*")] = 1
		k = 0
		n = len(sent)
		for tag, word in sent:
			k += 1
			# print word
			if is_rare_word(counter, word, tags):
				word = get_rare_class(word)
				#word = "_RARE_"
			for u in get_possible_tags(k - 1, tags, begin):
				for v in get_possible_tags(k, tags, begin):
					e_prob = counter.predict_emssiion_counts[(word, v)]
					# print word, v, e_prob
					if e_prob:
						max_pi = -1;
						max_tag = ""
						for w in get_possible_tags(k - 2, tags, begin):
							if k % 80 == 0: #fix to avoid out of float
								pi_w = pi[(k - 1, w, u)] * counter.trigram_prob[(w, u, v)] * e_prob * 1.0e100
							else:
								pi_w = pi[(k - 1, w, u)] * counter.trigram_prob[(w, u, v)] * e_prob
							#print word, pi_w, w, u, v
							if pi_w > max_pi:
								max_tag = w
								max_pi = pi_w
						pi[(k, u, v)] = max_pi
						#if max_tag == "":
							#print "maxtag == null", k, u, v
						pi_tag[(k, u, v)] = max_tag
						#print k, word, max_tag, u, v, max_pi
					else:
						pi[(k, u, v)] = 0
						pi_tag[(k, u, v)] = "-"
			
		
			
		max_tags = []
			
		max_pi = 0
		max_u = ""
		max_v = ""
		for u in get_possible_tags(n - 1, tags, begin):
			for v in get_possible_tags(n, tags, begin):
				pi_u_v = pi[(n, u, v)] * counter.trigram_prob[(u, v, "STOP")]
				#print n, u, v, pi[(n, u, v)], counter.trigram_prob[(u, v, "STOP")], pi_u_v
				if pi_u_v > max_pi:
					max_pi = pi_u_v
					max_u = u
					max_v = v
			
		
		max_tags.append(max_v)
		max_tags.append(max_u)
			
		
		for k in range(3, n + 1)[::-1]:
			l = len(max_tags)
			max_y = pi_tag[(k, max_tags[l - 1], max_tags[l - 2])]
			# print max_y, pi[(k,max_tags[l-1],max_tags[l-2])]
			max_tags.append(max_y)
			
		#print max_tags
		for k in range(0, n)[::-1]:
			tag = max_tags[k]
			word = sent[n - k - 1][1]
			output.write("%s %s\n" % (word, tag))
			
		output.write("\n")
	
def run_viterbi():
	counter = Hmm(3)
	input = file(sys.argv[1],"r")
	counter.read_counts(input)
	
	test_file = file(sys.argv[2],"r")
	viterbi(counter, test_file, sys.stdout)

if __name__ == "__main__":
	run_viterbi()
