#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : To generate directional imputed geometric features
#  Credit       : LEARNING FROM PROTEIN STRUCTURE WITH GEOMETRIC VECTOR PERCEPTRONS by Jing et al. 'The unit vector in the imputed direction of Cβi − Cαi' feature
#####################################################################################################################

import math
import numpy as np

def get_tetrahedral_geom(pos): #pos contains all positions
        last_res_no = int(pos[-1][22:(22+4)].strip())
        thg = [[[0,0,0],[0,0,0],[0,0,0]] for _ in range(last_res_no)]
      
        thg_val = [[0, 0, 0] for _ in range(last_res_no)]
      
        for i in range(len(pos)):
                res_no = int(pos[i][22:(22+4)].strip())
                atom_type = pos[i][13:(13+2)].strip()
                
                xyz = [float(pos[i][30:(30+8)]), float(pos[i][38:(38+8)]), float(pos[i][46:(46+8)])]
                if(atom_type == 'CA'):
                        thg[res_no-1][0] = xyz
                elif(atom_type == 'C'):
                        thg[res_no-1][1] = xyz 
                elif(atom_type == 'N'):
                        thg[res_no-1][2] = xyz  
        
        for i in range(len(thg_val)):
                N = np.array(thg[i][2])
                Ca = np.array(thg[i][0])
                C = np.array(thg[i][1])
                n = N - Ca
                c = C - Ca
                #n = [thg[i][2][0] - thg[i][0][0], thg[i][2][1] - thg[i][0][1], thg[i][2][2] - thg[i][0][2]]
                #c = [thg[i][1][0] - thg[i][0][0], thg[i][1][1] - thg[i][0][1], thg[i][1][2] - thg[i][0][2]]
                cross = np.cross(n,c)
                t1 = cross/((cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2) * math.sqrt(3))
                #summ = [n[0] + c[0], n[1] + c[1], n[2] + c[2]]
                summ = n + c
                t2 = math.sqrt(2/3) * summ / (summ[0] ** 2 + summ[1] ** 2 + summ[2] ** 2)
                thg_val[i] = t1 - t2 #[t1[0] - t2[0],  t1[1] - t2[1], t1[2] - t2[2]]
                if(np.isnan(thg_val[i]).any()):
                        thg_val[i] = [0,0,0] 
        return thg_val









































        
        
