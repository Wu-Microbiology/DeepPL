This repository includes the implementation of 'DeepPL ....'. Please cite our paper if you use the models or codes. The repo is still actively under development, so please kindly report if there is any issue encountered.

In this repository, we provide batch scripts to prepare training data for model training, including a script to check genome fasta files, a script to convert genome fasta files to kmer6 tsv files, and a script to process test results.
 
We also provide a prediction script predict_lyso_vs_lytic.py which takes a phage complete genome fasta file as input, produces a classification result on whether the input is a lysogenic or lytic phage.

Citation
If you have used DeepPL in your research, please kindly cite the following publication:
"......."


1. Environment setup

We used DNABERT which is build on top of huggingface transformer code to train out DeepPL model. The prediction script also needs the DNABERT conda environment to run.

Please follow the instructions at https://github.com/jerryji1993/DNABERT to install DNABERT  

2. Model download

Our lysogenic vs. lytic phage classification model can be downloaded at ....

3. To run prediction

conda activate dnabert

python predict_lyso_vs_lytic.py --dnabert_path path_to_the_DNABERT_installation_directory --model_path path_to_the_downloaded_model_directory --fasta_file input_phage_complete_genome.
