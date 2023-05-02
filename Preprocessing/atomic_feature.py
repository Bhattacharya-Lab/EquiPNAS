#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : This program calculates the volume and area of virtual convex hull formed by all-atoms in residues
#####################################################################################################################

from scipy.spatial import ConvexHull
import numpy as np

def get_residue_area_volume(pos):
        last_res_no = int(pos[-1][22:(22+4)].strip())
        res_coords = [[] for _ in range(last_res_no)]
        area = [0 for _ in range(last_res_no)]
        vol = [0 for _ in range(last_res_no)]
        #print(res_coords)
        for i in range(len(pos)):
                res_no = int(pos[i][22:(22+4)].strip())
                res_coords[res_no-1].append([float(pos[i][30:(30+8)]), float(pos[i][38:(38+8)]), float(pos[i][46:(46+8)])])
         
        for index, res in enumerate(res_coords):
                #print(res)
                if(len(res) < 4):
                        continue
                hull = ConvexHull(res)
                vol[index] = hull.volume
                area[index] = hull.area
        return area, vol
        
                                
        








































        
        
