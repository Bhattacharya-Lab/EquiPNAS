##################################################################################
#  Date created : 10/21/2022
#  Date modified: 10/21/2022 
#  Purpose      : Generate intermediate features from sequences and structures 
##################################################################################
import optparse, os, sys
from imputed_tetrahedral_geom_feature import *
parser=optparse.OptionParser()
parser.add_option('-t', dest='t',
        default= '',    #default empty!
        help= 'target list')
(options,args) = parser.parse_args()
target = options.t

f = open(target, 'r')
flines = f.readlines()
for line in flines:
        name = line.split('.')[0]
        
        
        os.system('python extract_dssp_feat.py  -i input/' + name + '.dssp -o tmp/'+name+'.feat')
        os.system('python extract_dssp_feat2.py  -i input/' + name + '.dssp -o tmp/'+name+'.feat2')
        os.system('python pdb2rr.py -t 8 -p input/'+name+'.pdb -o tmp/'+name+'.pdb2rr') 
        os.system('python prepare_25normal_contactcount.py --aa input/' + name + '.fasta --rr tmp/'+ name + '.pdb2rr --o tmp/' + name + '.concount')  
        os.system('python prepare_pdb_feature.py  --dssp_feat tmp/' + name + '.feat --input_monomer input/' + name + '.pdb --o tmp/' + name + '.feat')
        os.system('python prepare_pdb_feature1cd8ss8sa5angle.py  --dssp_feat tmp/' + name + '.feat2 --o tmp/' + name + '.feat22')
        os.system('python prepare_pdb_feature_phi_psi_alpha_sin_cos.py  --dssp_feat tmp/' + name + '.feat2 --o tmp/' + name + '.feat_angle6')
        os.system('python prepare_pdb_feature_rev_frwd_ca.py  --dssp_feat tmp/' + name + '.feat2 --o tmp/' + name + '.feat_forw_rev_ca6')
        
        fm = open('input/' + name  + '.pdb')
        fmlines = fm.readlines()
        pos = []
        for line in fmlines:
                if(line[:4] == 'ATOM'):
                        pos.append(line)
        dhg_val = get_tetrahedral_geom(pos)
        np.save('tmp/' + name + '.imputed3', dhg_val)
        fm.close()

 
