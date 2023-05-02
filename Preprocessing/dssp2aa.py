#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : This program obtains fasta (aa) from DSSP file
#####################################################################################################################

import os,sys
import optparse

parser=optparse.OptionParser()
parser.add_option('-i', dest='dssp_file',
        default= '',    #default empty!
        help= 'name of target')
parser.add_option('-o', dest='o',
        default= '',    #default empth
        help= 'name of output fasta file')

(options,args) = parser.parse_args()
dssp_file = options.dssp_file
out = options.o

faa = open(out , 'w')
faa.write('>' + out + '\n')

def read_dssp(dssp_file):
        if os.path.exists(dssp_file):
                with open(dssp_file) as fp:
                        lines = fp.readlines()
                        line = fp.readline()
                        lastresnum = int(lines[-1][5:10])
                        aalist = ['A' for _ in range(lastresnum)]
                        cntLn = 0 ##line counter##
                        residue="#"
                        count = 1
                        for line in lines:
                                if (cntLn<1):
                                        if (line[2:(2+len(residue))] == residue):
                                                cntLn+=1
                                                continue
                                if (cntLn>0):
                                        if (len(line)>0):
                                                aaSeq = line[13]
                                                resNum = (line[5:10].strip())
                                                if(resNum == ''):
                                                        continue
                                                resNum = int(resNum)
                                                aalist[resNum-1] = aaSeq
                        
                        #print(aalist) 
                        for aa in aalist:
                                faa.write(aa)
                                          
                fp.close()
        else:
                sys.stdout.write("\n dssp file for the target : " + template + "is missing\n")

read_dssp(dssp_file)
faa.close()
