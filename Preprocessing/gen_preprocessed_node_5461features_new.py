#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022
#  Purpose      : To generate (full) node feature set from temporary features
#####################################################################################################################

import optparse, os, sys
import numpy as np
parser=optparse.OptionParser()
parser.add_option('-t', dest='t',
        default= '',    #default empty!
        help= 'target list')
(options,args) = parser.parse_args()
target = options.t
def sigmoid(x):
    return 1/(1 + np.exp(-x))

f = open(target, 'r')
flines = f.readlines()
for line in flines:
                tgt = line.split('.')[0]
                print(tgt)
                name = tgt
                #tgtdata = []

                pdbfeat = np.load('tmp//' + name +'.feat.npy')
                pdbfeat2 = np.load('tmp//' + name + '.feat22.npy')
                pssmfeat = np.load('tmp//' + tgt + '.npy')
                ccountfeat = np.load('tmp//' + name +'.concount.npy')
                pdbsincosangle = np.load('tmp//' + name +'.feat_angle6.npy')
                pdbforwrevca = np.load('tmp//' +  name +'.feat_forw_rev_ca6.npy')
                pdbimputed = np.load('tmp//' + name +'.imputed3.npy')
                esm2feat = np.load('input/' + name + '.rep_5120.npy')

                feat33 = sigmoid(esm2feat[1:-1])
                singlefeat = np.load('input/'+ name + 'msa_first_row.npy')

                maxlen = max(len(pdbfeat), len(pssmfeat))
                singlefeat = sigmoid(singlefeat[:maxlen])
                #tgtdata = [[0 for _ in range(85)] for _ in range(maxlen)]
                tgtdata = np.zeros((maxlen, 5461))
                for ii in range(min(len(pdbfeat), len(pssmfeat))):
                        res = np.concatenate((pdbfeat[ii][:26], [pdbfeat[ii][27]], [ccountfeat[ii]], pdbfeat2[ii], pdbsincosangle[ii], pdbforwrevca[ii], pdbimputed[ii], pssmfeat[ii], feat33[ii], singlefeat[ii]))
                        #res_label = np.concatenate((res, label[ii]))
                        tgtdata[ii] = res
                #tgtdata = np.array(tgtdata)
                np.save('processed_features/' + tgt + '.5461featnew', tgtdata)
#alldata = np.array(alldata)
#np.save(o, alldata)

f.close()

