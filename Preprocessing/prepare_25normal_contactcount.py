#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : To generate contact count feature
#####################################################################################################################

import os,sys
import optparse
import numpy as np
from atomic_feature import get_residue_area_volume

parser=optparse.OptionParser()
parser.add_option('--rr', dest='rr',
        default= '',    #default empty!
        help= 'name of rr file')
parser.add_option('--aa', dest='aa',
        default= '',    #default empty!
        help= 'name of fasta file')

parser.add_option('--o', dest='o',
        default= '',    #default empth
        help= 'name of output feature file npz format')

(options,args) = parser.parse_args()
rr = options.rr
o = options.o
aa = options.aa
fd = open(aa, 'r')
fdr = open(rr, 'r')

fdlines = fd.readlines()
fdrlines = fdr.readlines()
N = len(fdlines[1].strip())
print(N)

countlist = [0 for _ in range(N)]
for line in fdrlines:
        res1 = line.split()[0]
        res2 = line.split()[1]
        if((int(res1) > N) or (int(res2) > N)):
                continue
        countlist[int(res1)-1] += 1
        countlist[int(res2)-1] += 1   
fd.close()
fdr.close()
#ff.close()
#print(countlist)
for i in range(len(countlist)):
        if (countlist[i] > 25):
                countlist[i] = 1
        else:
                countlist[i] /= 25
np.save(o, countlist)
