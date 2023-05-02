#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : To extract feature from DSSP file
#####################################################################################################################

import os,sys
import optparse

parser=optparse.OptionParser()
parser.add_option('-i', dest='dssp_file',
        default= '',    #default empty!
        help= 'name of target')
parser.add_option('-o', dest='o',
        default= '',    #default empth
        help= 'name of output feature file')

(options,args) = parser.parse_args()
dssp_file = options.dssp_file
o = options.o
ffeat = open(o, 'w')
ffeat.write('res\taa\tss\tsa\n')     

fi = open(dssp_file, 'r')
filines = fi.readlines()

cntLn = 0 ##line counter##
residue = '#'
count = 1
for line in filines:
        if(cntLn<1):  
                if (line[2:(2+len(residue))] == residue):  
                        cntLn+=1
                        continue
        if(cntLn>0):  
                if (len(line)>0):   
                        ssSeq = line[16:(16+1)]  
                        aaSeq = line[13]    
                        saSeq = line[35:(35+3)]     
                        if(ssSeq.strip() == ''): 
                                ssSeq = 'C'
                        if(line[5:10].strip() != ""):
                                resNum = int(line[5:10])  
                                ffeat.write(str(resNum) + '\t' + aaSeq + '\t' + ssSeq + '\t' + saSeq + '\n')     

fi.close()
ffeat.close()

