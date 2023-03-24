import sys

def check_actg(seq):
    ret = ""
    for x in range(len(seq)):
        if seq[x] not in "ACTG":
            ret = ret + seq[x]
    return ret

with open(sys.argv[1]) as ins:
    for line in ins:
        line = line.strip()
        s = ""
        with open(line) as ins2:
            for line2 in ins2:
                if ">" in line2:
                    continue
                line2 = line2.strip()
                t = check_actg(line2)
                if t != "":
                    print (line, "contains", t)
                else:
                    s += line2
        if len(s) == 0:
            print (line, "empty")
