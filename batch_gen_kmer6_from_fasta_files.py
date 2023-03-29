import sys

def seq2kmer(seq, k):
    """
    Convert original sequence to kmers
    
    Arguments:
    seq -- str, original sequence.
    k -- int, kmer of length k specified.
    
    Returns:
    kmers -- str, kmers separated by space

    """
    kmer = [seq[x:x+k] for x in range(len(seq)+1-k)]
    kmers = " ".join(kmer)
    return kmers

def check_actg(seq):
    for x in range(len(seq)):
        if seq[x] not in "ACTG":
            return False
    return True

k = 6
lyso_step = 1
lytic_step = 91

seq_len = int(sys.argv[2]) + k - 1
c1 = 0
c2 = 0
with open(sys.argv[1]) as ins:
    for line in ins:
        line = line.strip()
        actg = ""
        if "ysogenic" in line:
            label = 1
            step = lyso_step
        else:
            label = 0
            step = lytic_step
        c2 = c1
        with open(line) as ins2:
            for line2 in ins2:
                line2 = line2.strip()
                if ">" in line2:
                    continue
                if check_actg(line2):
                    actg += line2
        if len(actg) > 0:
            n = 0
            while n + seq_len < len(actg):
                kmers = seq2kmer(actg[n:n+seq_len], k)
                c1 += 1
                if sys.argv[3] == "s":
                    print ("{}\t{}".format(kmers, label))
                n += step
            actg = ""
        if sys.argv[3] == "l":
            print ("{}\t{}\t{}\t{}".format(label, c2, c1, line))
        if sys.argv[3] == "c":
            print ("{}\t{}\t{}".format(label, line, c1-c2))
            if c1 == c2:
                print (line, "ERROR")
