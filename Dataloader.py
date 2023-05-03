#####################################################################################################################
#  Date created : 10/21/2022
#  Date modified: 5/3/2023
#  Purpose      : This program reads and loads inputs data and passes them to the inference program
#####################################################################################################################

import dgl
import torch as trc
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dgl.dataloading import GraphDataLoader
from dgl.data import DGLDataset
import json
import random
class buildGraph(DGLDataset):
    #node_feature_size = 1365
    def __init__(self, indir):
        self.indir = indir

        super().__init__(name='buildgraph')


    def process(self):
        self.data_feats = []
        testlist = self.indir + '/input.list' 
        
        node_feat_dir = self.indir + '/processed_features/'
        edge_dir = self.indir + '/distmaps/'
        node_xyz_dir = self.indir + '/input/'
        f = open(testlist, 'r')
        flines = f.readlines()
        f.close()
        for line in flines:
            tgt = line.split('.')[0]
            #tgt = tgt.strip()
            labels = []
            featfile = np.load(node_feat_dir + tgt + '.5461featnew.npy', allow_pickle=True)
            nodeFeats = trc.Tensor(featfile)



            #### Create edge ####
            nodesLeft = []
            nodesRight = []
            src = []
            dst = []
            w = []

            
            rrfile = open(edge_dir + tgt + '.dist', 'r')
            rrlines = rrfile.readlines()
            w = []
            ### Sanity check: if no contact found, skip the target
            if(len(rrlines[1:]) == 0):
                print('No contact/distance found! Cannot create Graph! Skipping the target ... !')     
                continue
            for rline in rrlines[1:]:
                
                ni = int(rline.split()[0])-1
                nj = int(rline.split()[1])-1

                #sanity check
                if((ni >= len(nodeFeats)) or (nj >= len(nodeFeats))):
                    continue
                d = float(rline.split()[4])
                weight = np.log(abs(ni-nj))/d
                w.append([weight])
                w.append([weight])
                #making bi-directional edge
                nodesLeft.append(ni)
                nodesRight.append(nj)
                nodesLeft.append(nj)
                nodesRight.append(ni)
            rrfile.close()
            src = nodesLeft
            dst = nodesRight
            xyz_f = open(node_xyz_dir + tgt + '.pdb')
            
            xyz_ca = [[0,0,0] for _ in range(len(nodeFeats))]
            xyz_flines = xyz_f.readlines()
            for xyzline in xyz_flines:
                if(xyzline[:4] == "ATOM" and xyzline[12:16].strip() == "CA"):
                    x = float(xyzline[30:38].strip())
                    y = float(xyzline[38:46].strip())
                    z = float(xyzline[46:54].strip())

                    res_no = int(xyzline[22:(22+4)]) - 1
                    if(res_no >= len(xyz_ca)):
                        continue
                    xyz_ca[res_no] = [x, y, z]
            xyz_f.close()
            xyz_ca = np.array((xyz_ca))
            
            
            edges = [src, dst]
            src = np.array(src)
            dst = np.array(dst)
            w = np.array(w)      
            #print(xyz_ca.shape)
            xyz_feats = xyz_ca.astype(np.float32)
            xyz_feats = trc.Tensor(xyz_feats)
            #labels = np.array(labels).astype(np.float32)
            self.labels = trc.Tensor([labels])            

            ### sanity check ndata length should match
            if(len(nodeFeats) != len(xyz_feats)):
                print('Node length mismatch with xyz ! Considering the minimum ... !')
                print(len(nodeFeats))
                print(len(xyz_feats))
                nodeFeats = nodeFeats[:len(xyz_feats)]
                xyz_feats = xyz_feats[:len(nodeFeats)]
            self.tgt = tgt
            self.nodeFeats = nodeFeats
            self.xyz_feats = xyz_feats
            self.edge_att = trc.LongTensor(w)
            self.edges = [trc.LongTensor(edges[0]), trc.LongTensor(edges[1])]
            self.data_feats.append((self.tgt, self.nodeFeats, self.xyz_feats, self.edges, self.edge_att))

            

    def __getitem__(self, i):
        return self.data_feats[i]

    def __len__(self):
        return len(self.data_feats)

