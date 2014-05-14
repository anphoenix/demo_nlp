demo_nlp
========

1.Tagging Demo using HMM (in python) in ./hmm 

	The task consists of identifying gene names within biological text
	In this dataset there is one type of entity:gene (GENE). The dataset is adapted from the BioCreAtIvE II shared task (http://biocreative.sourceforge.net/biocreative_2.html).

Usage:

0. clean the training data with smooth method	

		mkdir demo
		python prepare_training_data.py data/gene.train > demo/gene.train.refine

1. create HMM model (language model and language/tag transit probability model)

		python count_freqs.py demo/gene.train.refine > demo/gene.counts

2. Run Viterbi to tagging the test data

		python emission_parameter.py demo/gene.counts data/gene.dev > demo/gene.value

3. evaluate the tagging result
	
		python eval_gene_tagger.py data/gene.key demo/gene.value
		
	You will got the final result of the HMM Tagger
	
		Found 413 GENEs. Expected 642 GENEs; Correct: 222.
			 	precision 	recall 		F1-Score
		GENE:	 0.537530	0.345794	0.420853

2.HMM Tagger used as Chinese Tokenizer

Usage:

0. generate training data and test data [Need Refine to Random Selection]

		python msr_data_cleaner.py training msr_training.utf8 data/training 8000
		python msr_data_cleaner.py test msr_training.utf8 data/test 8000
		#test data will generate two file: test.key is the un-tagged file, and test.val is the tagged file

1. generate HMM model using ../hmm tool

		python ../hmm/count_freqs.py data/training > model/model.counts

2. perform the tokenize on test data

		python ../hmm/emission_parameter.py model/model.counts data/test.key > data/test.out

3. compare the machine tagging tokenization result with test result