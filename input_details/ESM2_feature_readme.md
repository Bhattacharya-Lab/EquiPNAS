Download and install ESM2 from [here](https://github.com/facebookresearch/esm)

Copy the [feature generation script](https://github.com/Bhattacharya-Lab/EquiPPIS/blob/main//Preprocessing/supporting_scripts/ESM2_features.py) inside `esm/esm/`

Run the ESM2-feature generation script

`python esm2_feature.py -i your_input_fasta.fasta -o target_esm2_feature.esm2_33`

The output ESM2-featue will be saved as `target_esm2_feature.esm2_33.npy`
