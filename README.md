
![AI-Figure 1-04-07-2023](https://user-images.githubusercontent.com/124622531/230945786-7a3372ae-d8fd-471a-a3bf-785f89d396c4.jpg)

This repository includes the implementation of 'DeepPL ....'. Please cite our paper if you use our model or code. The repo is still actively under development, please let us know if you encounter and issues.

In this repository, we provide batch scripts to prepare training data for model training, including a script to check genome fasta files, a script to convert genome fasta files to kmer6 tsv files, and a script to process test results.
 
We also provide a prediction script predict_lyso_vs_lytic.py which takes a phage complete genome fasta file as input, produces a classification result on whether the input is a lysogenic or lytic phage.

Citation. If you have used DeepPL in your research, please kindly cite the following publication:
"......."


1. Environment setup

We used DNABERT which is build on top of huggingface transformer code to train out DeepPL model. The prediction script also needs the DNABERT conda environment to run.

Please follow the instructions at https://github.com/jerryji1993/DNABERT to install DNABERT and setup the dnabert conda environment.

2. Model download

Our lysogenic vs. lytic phage classification model can be downloaded at https://drive.google.com/file/d/1PzQOi8QQDV6IBOBya-3I5zj1UFj4RA1S/view?usp=sharing

3. To run prediction

conda activate dnabert

cd DeepPL

python predict_lyso_vs_lytic.py --model_path path_to_the_downloaded_model_directory --fasta_file input_phage_complete_genome.
