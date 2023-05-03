######################################################################################################################################################
#      This program generates Lx5120 feature embedding from an input fasta and outputs in npy format                                                 #
#      Credit: Meta Platforms, Inc. and affiliates,                                                                                                  #
#      colab notebook :    https://github.com/facebookresearch/esm/blob/main/examples/esm2_infer_fairscale_fsdp_cpu_offloading.py                    #
######################################################################################################################################################

import esm
import torch
import os
from Bio import SeqIO
import itertools
from typing import List, Tuple
import string
import numpy
torch.set_grad_enabled(False)
import numpy as np
import operator
import numpy as np
import optparse

parser=optparse.OptionParser()
parser.add_option('-i', dest='in_seq',
        default= '',    #default empty!'
        help= 'Input alignment')
parser.add_option('-o', dest='out_npy',
        default= '',    #default empty!'
        help= 'output alignment embed feature')

(options,args) = parser.parse_args()

in_seq = options.in_seq
out_npy = options.out_npy

deletekeys = dict.fromkeys(string.ascii_lowercase)
deletekeys["."] = None
deletekeys["*"] = None
translation = str.maketrans(deletekeys)

def read_sequence(filename: str) -> Tuple[str, str]:
    """ Reads the first (reference) sequences from a fasta or MSA file."""
    record = next(SeqIO.parse(filename, "fasta"))
    print(record)
    return record.description, str(record.seq)

def remove_insertions(sequence: str) -> str:
    """ Removes any insertions into the sequence. Needed to load aligned sequences in an MSA. """
    return sequence.translate(translation)

def read_msa(filename: str, nseq: int) -> List[Tuple[str, str]]:
    """ Reads the first nseq sequences from an MSA file, automatically removes insertions."""
    return [(record.description, remove_insertions(str(record.seq)))
            for record in itertools.islice(SeqIO.parse(filename, "fasta"), nseq)]

# Load ESM-2 model
model, alphabet = esm.pretrained.esm2_t48_15B_UR50D()
batch_converter = alphabet.get_batch_converter()
model.eval()  # disables dropout for deterministic results
data = [
    read_sequence(in_seq)]

batch_labels, batch_strs, batch_tokens = batch_converter(data)

# Extract per-residue representations (on CPU)
with torch.no_grad():
    results = model(batch_tokens, repr_layers=[48], return_contacts=True)
token_representations = results["representations"][48]
#print(token_representations[0].shape)
np.save(out_npy, token_representations[0])   

