demo_nlp
========

1. Tagging Demo using HMM (in python) in ./hmm 

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

