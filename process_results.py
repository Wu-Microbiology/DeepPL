import sys
import numpy as np

r1 = np.load(sys.argv[1])
print("dim:", r1.shape)
r2 = np.load(sys.argv[2])
print("dim:", r2.shape)
r = np.zeros(r1.shape[0] + r2.shape[0])
s1 = int (r1.shape[0] / 2)
s2 = int (r2.shape[0])
r[0:s1] = r1[0:s1]
r[s1:s1+s2] = r2
r[s1+s2:] = r1[s1:]
#sys.exit(0)

err = 0
tot = 0

thresh1 = 0.9
#500
#thresh2 = 0.05
#100,200
thresh2 = 0.016

dict1 = {}
dict2 = {}
print ("threshold1:", thresh1, "threshold2:", thresh2)
with open(sys.argv[3]) as ins:
    for line in ins:
        tot += 1
        line = line.strip()
        vals = line.split('\t')
        l = int(vals[0])
#        l = 0
        s = int(vals[1])
        e = int(vals[2])
        p = np.sum(((r[s:e]))>thresh1)/(e-s)
        if (p >= thresh2 and l == 0) or (p < thresh2 and l == 1):
            err += 1
            err_str = "ERROR!\t"
        else:
            err_str = ""
#        err = 0
#        err_str = ""
        if p >= thresh2:
            out = "Predict:Lysogenic"
        else:
            out = "Predict:Lytic    "
        out = "{}{}\t{}\t{}".format(err_str, out, p, line)
        if l == 1:
            if p in dict1:
                dict1[p] += "\n" + out
            else:
                dict1[p] = out
        else:
            if p in dict2:
                dict2[p] += "\n" + out
            else:
                dict2[p] = out
print("Error:", err, "Total:", tot, "Error rate:", err/tot, "\n")

for p in sorted(dict1):
    print(dict1[p])
for p in sorted(dict2):
    print(dict2[p])
