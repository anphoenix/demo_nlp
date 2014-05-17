demo_nlp
========

1.Tagging Demo using HMM (in python) in ./hmm 

	The task consists of identifying gene names within biological text
	In this dataset there is one type of entity:gene (GENE). The dataset is adapted from the BioCreAtIvE II shared task (http://biocreative.sourceforge.net/biocreative_2.html).

Usage:

0. clean the training data with smooth method	

		mkdir demo
		python data_cleaner.py data/gene.train > demo/gene.train.refine

1. create HMM model (language model and language/tag transit probability model)

		python hmm_trainer.py demo/gene.train.refine > demo/gene.counts

2. Run Viterbi to tagging the test data

		python hmm_scorer.py demo/gene.counts data/gene.dev > demo/gene.value

3. evaluate the tagging result
	
		python eval_gene_tagger.py data/gene.key demo/gene.value
		
	You will got the final result of the HMM Tagger
	
		Found 413 GENEs. Expected 642 GENEs; Correct: 222.
			 	precision 	recall 		F1-Score
		GENE:	 0.537530	0.345794	0.420853

2.HMM Tagger used as Chinese Tokenizer

Usage:

0. generate training data and test data: following comments is using icwb dataset, available at http://www.sighan.org/bakeoff2005/
   and put the data in icwb2-data folder

		python data_cleaner_icwb.py training icwb2-data/training/msr_training.utf8 data/training 86924
		python data_cleaner_icwb.py test icwb2-data/gold/msr_test_gold.utf8 data/test 3985
		#test data will generate two file: test.key is the un-tagged file, and test.val is the tagged file

1. generate HMM model using ../hmm tool

		python ../hmm/hmm_trainer.py data/training > model/model.counts

2. perform the tokenize on test data

		python ../hmm/hmm_scorer.py model/model.counts data/test.key > data/test.out

3. generate icwb format result data

        python result_formatter.py data/test.out > data/formatted_test.out

4. compare the machine tagging tokenization result with test result

Previous implementation only use two tags: B and I to format the training data. To enhance we use four tag to format the training data:
	S is a simple charater word, for long word, B is tag for the beginning, M is tag for middle, and E is tag for the end.
		
		python data_cleaner_icwb.py training icwb2-data/training/msr_training.utf8 data/training 86924 4
		python data_cleaner_icwb.py test icwb2-data/gold/msr_test_gold.utf8 data/test 3985 4
	
