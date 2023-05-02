#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : To generate Cb-Cb contact/distance map from PDB for a threshold
#####################################################################################################################

import os,math
import optparse    # for option sorting

parser = optparse.OptionParser()

parser.add_option('-p', dest='p',
        default = '',    # default empty
        help = 'pdb file')
parser.add_option('-o', dest='o',
        default = '',    # default empty
        help = 'output rr name')

parser.add_option('-t', dest='t',
        default = '',    # default empty
        help = 'distance threshold')


(options,args) = parser.parse_args()
p = options.p
out = options.o
th = float(options.t)




class OrientationAngles():
        """
        the class for rr
        """



        def __init__(self, p, out):
                #constructor, initializing values
                _, pdb_file1 = os.path.split(p)
                self.pdb_file1 = pdb_file1.split('.')[0]
                self.pdb_file = pdb_file1.split('_')[0]       
                self.p = p
                self.output = out

        def get_distance(self, x1, x2, x3, y1, y2, y3):
                return math.sqrt((x1 - y1) ** 2 + (x2 - y2) ** 2 + (x3 - y3) ** 2)


        def cal_orientation(self):
                fpdb1 = open(self.p, 'r') 
                f1lines = fpdb1.readlines()
               
                pos1 = []
                          
                for atomline in f1lines: 
                        if(atomline[:4] == 'ATOM'):  
                               
                                pos1.append(atomline) #[atomline[21], atomline[22:26].strip(), float(atomline[30:38].strip()), float(atomline[38:46].strip()), float(atomline[46:54].strip())])     
                fpdb1.close()
                             

                Ca_info = {}
                Cb_info = {}
                for line in pos1:
                        if(line[:4] == "ATOM"):
                                  
                              
                                Ca = []
                                Cb = []
                                res_no = 0
                                if(line[12:16].strip() == "CA"):
                                        x = float(line[30:38].strip())
                                        y = float(line[38:46].strip())
                                        z = float(line[46:54].strip())
                                        Ca = [x, y, z]
                                        res_no = int(line[22:26].strip())
                                        Ca_info[res_no] = Ca

                                if(line[12:16].strip() == "CB"):
                                        x = float(line[30:38].strip())
                                        y = float(line[38:46].strip())
                                        z = float(line[46:54].strip())
                                        Cb = [x, y, z]
                                        res_no = int(line[22:26].strip())
                                        Cb_info[res_no] = Cb

                fcb = open(self.output, "w")
                for res_no in (Ca_info):
                        for res_no2 in (Ca_info):
                                if(res_no2 < (res_no + 1)):
                                        continue
                                if ((res_no not in Cb_info) and (res_no2 not in Cb_info)):
                                        cb_cb_distance = self.get_distance(Ca_info[res_no][0], Ca_info[res_no][1],  Ca_info[res_no][2], Ca_info[res_no2][0], Ca_info[res_no2][1], Ca_info[res_no2][2])
                                elif((res_no in Cb_info) and (res_no2 not in Cb_info)):
                                        cb_cb_distance = self.get_distance(Cb_info[res_no][0], Cb_info[res_no][1],  Cb_info[res_no][2], Ca_info[res_no2][0], Ca_info[res_no2][1], Ca_info[res_no2][2])
                                
                                elif((res_no not in Cb_info) and (res_no2 in Cb_info)):
                                        cb_cb_distance = self.get_distance(Ca_info[res_no][0], Ca_info[res_no][1],  Ca_info[res_no][2], Cb_info[res_no2][0], Cb_info[res_no2][1], Cb_info[res_no2][2])
                                else:
                                        cb_cb_distance = self.get_distance(Cb_info[res_no][0], Cb_info[res_no][1],  Cb_info[res_no][2], Cb_info[res_no2][0], Cb_info[res_no2][1], Cb_info[res_no2][2])
                                if(cb_cb_distance > th):
                                        continue
                                
                                fcb.write(str(res_no) + ' ' + str(res_no2) + ' 0 8 ' + '%.1f'%cb_cb_distance +"\n")
                fcb.close()        

def main():
        orientation_angle = OrientationAngles(p, out)
        orientation_angle.cal_orientation()
        
       
        

if __name__ == "__main__":
        main()


