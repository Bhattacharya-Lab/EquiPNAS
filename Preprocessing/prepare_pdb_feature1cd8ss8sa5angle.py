#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : This program is to crate features from pdb (dssp) complementary ss, sa, angle features and relative spetial position of a residue
#####################################################################################################################


import os,sys
import optparse
import numpy as np
from atomic_feature import get_residue_area_volume
import math
parser=optparse.OptionParser()
parser.add_option('--dssp_feat', dest='dssp_feat',
        default= '',    #default empty!
        help= 'name of dssp feature file')
parser.add_option('--o', dest='o',
        default= '',    #default empth
        help= 'name of output feature file npz format')

(options,args) = parser.parse_args()
dssp_feat = options.dssp_feat
o = options.o

fd = open(dssp_feat, 'r')

fdlines = fd.readlines()

length = int(fdlines[-1].split()[0])
feature_list = [[0 for _ in range(22)] for _ in range(length)] # 1D feature dimension is set 28, may change

dssp_list = [[0 for _ in range(22)] for _ in range(length)]

def ss_one_hot8(ss):
        if(ss == 'H'): 
                return 1, 0, 0, 0, 0, 0, 0, 0
        elif(ss == 'G'):
                return 0, 1, 0, 0, 0, 0, 0, 0
        elif(ss == 'I'):
                return 0, 0, 1, 0, 0, 0, 0, 0      
        elif(ss == 'E'): 
                return 0, 0, 0, 1, 0, 0, 0, 0      
        elif(ss == 'B'): 
                return 0, 0, 0, 0, 1, 0, 0, 0  
        elif(ss == 'T'):
                return 0, 0, 0, 0, 0, 1, 0, 0
        elif(ss == 'S'):
                return 0, 0, 0, 0, 0, 0, 1, 0
        else:
                return 0, 0, 0, 0, 0, 0, 0, 1     

def sa_one_hot8(sa):
        if(float(sa) < 30):
                return 1, 0, 0, 0, 0, 0, 0, 0 
        elif(float(sa) < 60):
                return 0, 1, 0, 0, 0, 0, 0, 0
        elif(float(sa) < 90):
                return 0, 0, 1, 0, 0, 0, 0, 0
        elif(float(sa) < 120):
                return 0, 0, 0, 1, 0, 0, 0, 0
        elif(float(sa) < 150):
                return 0, 0, 0, 0, 1, 0, 0, 0
        elif(float(sa) < 180):
                return 0, 0, 0, 0, 0, 1, 0, 0
        elif(float(sa) < 210):
                return 0, 0, 0, 0, 0, 0, 1, 0
        else:
                return 0, 0, 0, 0, 0, 0, 0, 1


def dist(x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
def centroid(pos):
        cx = 0
        cy = 0
        cz = 0
        for i in range(len(pos)):
                cx += pos[i][0]
                cy += pos[i][1]
                cz += pos[i][2]
        cx /= len(pos)
        cy /= len(pos)
        cz /= len(pos)
        return cx, cy, cz

pos = []
for line in fdlines[1:]:
        line = line.strip().split()  
        x = float(line[9])
        y = float(line[10])
        z = float(line[11])
        pos.append([x, y, z])

#print(pos)
cx, cy, cz = centroid(pos)


for line in fdlines[1:]:
        line = line.strip().split()
        x = float(line[9])
        y = float(line[10])
        z = float(line[11])
        d = dist(x, y, z, cx, cy, cz)  
        d = 1/d
        #print(d)
        dssp_list[int(line[0]) - 1][0] = d #for d
        dssp_list[int(line[0]) - 1][1:(1+8)] = ss_one_hot8(line[2])
        dssp_list[int(line[0]) - 1][9:(9+8)] = sa_one_hot8(line[3])
        dssp_list[int(line[0]) - 1][17] = float(line[4]) 
        dssp_list[int(line[0]) - 1][18] = float(line[5])/360.0 
        dssp_list[int(line[0]) - 1][19] = float(line[6])/360.0
        dssp_list[int(line[0]) - 1][20] = float(line[7])/360.0  
        dssp_list[int(line[0]) - 1][21] = float(line[8])/360.0    

for i in range(len(feature_list)):
        feature_list[i] = dssp_list[i] #+ [inverse(areaA[i])] + [inverse(volA[i])] + [1/(i+1)] #last one is relative position
        #print(feature_list[i])

np.save(o, feature_list)
        
fd.close()
#fm.close()
