Download and install Evolutionary Scale Modeling (ESM) from [here](https://github.com/facebookresearch/esm)

Copy the [ESM-2 feature generation script](supporting_scripts/esm2_15B_rep_5120.py) inside `esm/`

Run the ESM-2 feature generation script

`python esm2_15B_rep_5120.py -i your_input_fasta.fasta -o target_esm2_feature.rep_5120`

The output ESM-2 featue will be saved as `target_esm2_feature.rep_5120.npy`

An example ESM-2 representation feature can be found [here](../Preprocessing/input/4zm2_B.rep_5120.npy)

