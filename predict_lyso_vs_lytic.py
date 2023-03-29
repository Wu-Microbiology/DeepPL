import os
import sys
import numpy as np
import argparse

def check_actg(seq):
    ret = ""
    for x in range(len(seq)):
        if seq[x] not in "ACTG":
            ret = ret + seq[x]
    return ret

def seq2kmer(seq, k):
    kmer = [seq[x:x+k] for x in range(len(seq)+1-k)]
    kmers = " ".join(kmer)
    return kmers


parser = argparse.ArgumentParser()

parser.add_argument('--dnabert_path', type=str, required=True)
parser.add_argument('--model_path', type=str, required=True)
parser.add_argument('--fasta_file', type=str, required=True)

args = parser.parse_args()

with open(args.fasta_file) as ins:
    c = 0
    for line in ins:
        c += 1
        if c == 1:
            continue
        if c >= 3:
            break
        line = line.strip()
        t = check_actg(line)
        if t != "":
            print ("Error: fasta file contains letter", t, "expecting ACTG only")
            sys.exit(1)
        dna = line
if c != 2:
    print ("Error: expecting fasta file to contain 2 lines where the second line is the dna sequence.")
    sys.exit(1)

tmp_dir = "./" + args.fasta_file.split("/")[-1] + ".tmp"
if os.path.exists(tmp_dir):
    os.system("rm -r " + tmp_dir)
print ("Creating tmp directory:", tmp_dir)
os.system("mkdir " + tmp_dir)

k = 6
step = 1
seq_len = 100 + k - 1

n = 0
c = 0

with open(tmp_dir + "/dev.tsv", "w") as f:
    f.write("sequence\tlabel\n")
    while n + seq_len < len(dna):
        kmers = seq2kmer(dna[n:n+seq_len], k)
        f.write("{}\t{}\n".format(kmers, c % 2))
        n += step
        c += 1

run_finetune_command = "python {} --model_type dna --tokenizer_name=dna6 --model_name_or_path {} --task_name dnaprom --do_predict --data_dir {} --max_seq_length 100 --per_gpu_pred_batch_size=32 --output_dir {} --predict_dir {} --n_process 48".format(args.dnabert_path + "/examples/run_finetune.py", args.model_path, tmp_dir, args.model_path, tmp_dir)

print ("")
print (run_finetune_command)

os.system(run_finetune_command)
r = np.load(tmp_dir + "/pred_results.npy")

err = 0
tot = 0

thresh1 = 0.9
thresh2 = 0.016

dict1 = {}
dict2 = {}
print ("threshold1:", thresh1, "threshold2:", thresh2)

s = 0
e = r.shape[0]
p = np.sum(((r[s:e]))>thresh1)/(e-s)
if p >= thresh2:
    out = "Predict:Lysogenic"
else:
    out = "Predict:Lytic"

print (p, out)
