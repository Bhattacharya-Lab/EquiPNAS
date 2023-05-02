#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : To generate features from PSSM
#####################################################################################################################

import numpy as np
import os,sys
import os.path
#os.path.isfile(fname)
import optparse

parser=optparse.OptionParser()
parser.add_option('-i', dest='i',
        default= '',    #default empty!
        help= 'name of pssm directory')
parser.add_option('-o', dest='o',
        default= '',    #default empth
        help= 'output directory')
parser.add_option('-t', dest='t',
        default= '',    #default empth
        help= 'target list')

(options,args) = parser.parse_args()
inp = options.i
out = options.o
t = options.t
 
def sigmoid(X):
        return 1/(1+np.exp(-X))


filename = t
f = open(filename, 'r')
flines = f.readlines()

for line in flines:
        name = line.split('.')[0]
        #print(name)
        pssmarr = []
        if(os.path.isfile(inp + '/'+name+'.pssm') == False):
                continue
        print(name)
        fpssm = open(inp + '/' + name + '.pssm', 'r')
        fpssmlines = fpssm.readlines()
        for pssmline in fpssmlines[3:-6]:
                pssm20 = []
                pssmline = pssmline.split()
                #for ii in range(20):
                #        pssm20.append(pssmline[3*ii+9:3*ii+12])
                #pssm20 = pssmline.strip().split()
                pssm20 = pssmline[2:22]
                #print(pssm20)
                pssm20 = list(map(int, pssm20))
                  
                #print(str(pssm20))
                pssm20 = sigmoid(np.array(pssm20))
                #print(str(pssm20))
                pssmarr.append(pssm20)
        pssmarr = np.array(pssmarr)
        np.save(out + '/' + name, pssmarr)
                #print(str(pssm20))
        fpssm.close()
f.close()
