The purpose of this project is to run two gene prediction formats on a genome, then to compare the resultf of these gene predictors.

This project involves several functions.  

run_genemark() takes a genome name as a command line argument and runs genemarks.  It creates a file called genome.lst, where 'genome is the name of the genome provided.
run_glimmer() does the same.  Within this function, a tag corresponding to the genome name is created.  The result is afile called genome.predict.

construct_GMgenes() and construct_Glim_genes construct dictionaries holding the relevant info to be compared - gene name, strand, start, and stop

compare_GM_Glim then compares the two, listing the number of total genes, the number of + strand and - strand genes, the start sites specific to GM and to Glim, and the starts predicted by both
