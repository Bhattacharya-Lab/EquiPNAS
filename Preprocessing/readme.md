All input PDB chains, FASTA, [DSSP](../input_details/DSSP_readme.md), [PSSM](../input_details/PSSM_readme.md), [MSA first row](../input_details/MSA_first_row_readme.md), and [ESM-2 representation](../input_details/ESM-2_representation_readme.md) files should be inside `input/` directory

All distance maps should be inside `distmaps/`

Target list: `input.list`

1. Run `gen_aa_structural_features.py` (feature files will be saved in `tmp/` directory)

`python gen_aa_structural_features.py -t input.list`

2. Run `genpssmto20feat.py` (feature files will be saved in `tmp/` directory)

`python genpssmto20feat.py  -i input -o tmp/ -t input.list`

3. Run `gen_preprocessed_node_5461features_new.py`

`python gen_preprocessed_node_5461features_new.py -t input.list`
