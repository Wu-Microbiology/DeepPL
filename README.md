
![DeepPL Overview](https://github.com/user-attachments/assets/babba0f6-fd13-4758-86cd-c24c6a4b4a87)


This repository includes the implementation of 'DeepPL: a deep-learning-based tool for the prediction of bacteriophage lifecycle'. Please cite our paper if you use our model or code. The repo is still actively under development, please let us know if you encounter and issues.

In this repository, we provide batch scripts to prepare training data for model training, including a script to check genome fasta files, a script to convert genome fasta files to kmer6 tsv files, and a script to process test results.
 
We also provide a prediction script predict_lyso_vs_lytic.py which takes a phage complete genome fasta file as input, produces a classification result on whether the input is a lysogenic or lytic phage.

Citation. If you have used DeepPL in your research, please kindly cite the following publication:
```
"Zhang Y, Mao M, Zhang R, Liao Y-T, Wu VCH (2024) DeepPL: A deep-learning-based tool for the prediction of bacteriophage lifecycle. PLoS Comput Biol 20(10): e1012525. https://doi.org/10.1371/journal.pcbi.1012525"
```

1. Environment setup

We used DNABERT which is build on top of huggingface transformer code to train out DeepPL model. The prediction script also needs the DNABERT conda environment to run.

Please follow the instructions at https://github.com/jerryji1993/DNABERT to install DNABERT and setup the dnabert conda environment.

```
conda env create -f deeppl-linux.yml --prefix path_to_conda_environment/deeppl
```

2. Model download

Our lysogenic vs. lytic phage classification model can be directly downloaded at google drive (https://drive.google.com/file/d/1PzQOi8QQDV6IBOBya-3I5zj1UFj4RA1S/view?usp=sharing) or figshare (https://figshare.com/articles/software/DeepPL_model/27005053?file=49153420).


3. To run prediction
```
conda activate deeppl
cd DeepPL
python predict_lyso_vs_lytic.py --model_path path_to_the_downloaded_model_directory --fasta_file input_phage_complete_genome
```
