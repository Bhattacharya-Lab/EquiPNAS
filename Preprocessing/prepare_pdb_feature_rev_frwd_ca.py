#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : This program is to crate features for forward and reverse direction to next and previous Ca-Ca total 6               
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


for linei in range(2, len(fdlines)-1):
        line = fdlines[linei].split()
        line_prev = fdlines[linei-1].split()
        line_post = fdlines[linei+1].split()
        res = int(line[0]) - 1
        cai = [float(line[9]), float(line[10]), float(line[11])]
        cai_prev = [float(line_prev[9]), float(line_prev[10]), float(line_prev[11])]
        cai_post = [float(line_post[9]), float(line_post[10]), float(line_post[11])]
        forw = np.subtract(cai_post, cai)
        revw = np.subtract(cai_prev, cai)

        forwn = math.sqrt(forw[0] ** 2 + forw[1] ** 2 +  forw[2] ** 2)
        revwn = math.sqrt(revw[0] ** 2 + revw[1] ** 2 +  revw[2] ** 2)

        u_forw = forw/forwn
        u_revw = revw/revwn
        #print(u_forw, u_revw)
        
        feature_list[res][:3] = u_forw 
        feature_list[res][3:] = u_revw
        #print(feature_list[res])


np.save(o, feature_list)
        
fd.close()
#fm.close()
