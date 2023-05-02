#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : This program is to crate features from pdb phi-psi-alpha (sin,cos) total 6     
#####################################################################################################################
import os,sys
import optparse
import numpy as np
import math
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
feature_list = [[0 for _ in range(6)] for _ in range(length)] # 1D feature dimension is set 6, may change


for line in fdlines[1:]:
        line = line.strip().split()
        res = int(line[0]) - 1
        alpha = float(line[6])
        phi = float(line[7])  
        psi = float(line[8])
        alphasin = math.sin(math.radians(alpha))
        alphacos = math.cos(math.radians(alpha))
        phisin = math.sin(math.radians(phi))
        phicos = math.cos(math.radians(phi))
        psisin = math.sin(math.radians(psi))
        psicos = math.cos(math.radians(psi))
        feature_list[res] = [alphasin, alphacos, phisin, phicos, psisin, psicos]



np.save(o, feature_list)
        
fd.close()
#fm.close()
