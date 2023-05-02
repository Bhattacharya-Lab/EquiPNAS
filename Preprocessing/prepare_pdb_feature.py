#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : This program is to crate features from pdb, 25 features from dssp, 2 features from convex hull atoms volume and surface area, 1 feature from relative position
#####################################################################################################################

import os,sys
import optparse
import numpy as np
from atomic_feature import get_residue_area_volume

parser=optparse.OptionParser()
parser.add_option('--dssp_feat', dest='dssp_feat',
        default= '',    #default empty!
        help= 'name of dssp feature file')
parser.add_option('--input_monomer', dest='input_monomer',
        default= '',    #default empty!
        help= 'name of input monomer file')
parser.add_option('--o', dest='o',
        default= '',    #default empth
        help= 'name of output feature file npz format')

(options,args) = parser.parse_args()
dssp_feat = options.dssp_feat
input_monomer = options.input_monomer
o = options.o

fd = open(dssp_feat, 'r')
fm = open(input_monomer, 'r')

fdlines = fd.readlines()
fmlines = fm.readlines()

length = int(fdlines[-1].split()[0])
feature_list = [[0 for _ in range(28)] for _ in range(length)] # 1D feature dimension is set 28, may change

### get atomic features ###
pos = []
for line in fmlines:
        if(line[:4] == 'ATOM'):
                pos.append(line.strip())

areaA, volA = get_residue_area_volume(pos)

if(len(areaA) != length):
        print('length mismatch!!!!')
        print(dssp_feat)
        print(len(areaA))
        print(length)

### get dssp features (aa, ss, sa, ...)
dssp_list = [[0 for _ in range(25)] for _ in range(length)]
amino_acids = {'A':0, 'R':1, 'N':2, 'D':3, 'C':4, 'Q':5, 'E':6, 'G':7, 'H':8, 'I':9, 'L':10, 'K':11, 'M':12, 'F':13, 'P':14, 'S':15, 'T':16, 'W':17, 'Y':18, 'V':19}

def ss_one_hot3(ss):
        if(ss == 'H' or ss == 'G' or ss == 'I'): #helix
                return 1, 0, 0
        elif(ss == 'E' or ss == 'B'):
                return 0, 1, 0
        else:
                return 0, 0, 1

def sa_one_hot2(sa):
        if(float(sa) > 50):
                return 1, 0 #solvant acc
        else:
                return 0, 1
def sigmoid(X):
        return 1/(1+np.exp(-X))

def inverse(X):
        if(X < 1):
                return 0
        else:
                return 1/X
for line in fdlines[1:]:
        line = line.strip().split()
        #print(line[1] + str(amino_acids[line[1]]))      
        if(line[1] not in amino_acids):
                print('not in aminoacids')
                print(line[1])
                dssp_list[int(line[0]) - 1][0] = 1
        else: 
                dssp_list[int(line[0]) - 1][amino_acids[line[1]]] = 1 #for aa
        #print(line[1] + str(amino_acids[line[1]]))
        dssp_list[int(line[0]) - 1][20:(20+3)] = ss_one_hot3(line[2])
        dssp_list[int(line[0]) - 1][23:(23+2)] = sa_one_hot2(line[3])

for i in range(len(feature_list)):
        feature_list[i] = dssp_list[i] + [inverse(areaA[i])] + [inverse(volA[i])] + [1/(i+1)] #last one is relative position
        #print(feature_list[i])

np.save(o, feature_list)
        
fd.close()
fm.close()
