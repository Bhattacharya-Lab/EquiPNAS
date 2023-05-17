
Download and install ColabFold from [here](https://github.com/sokrypton/ColabFold/)

Copy [this](supporting_scripts/batch_save_msa_feat.py) feature generation script `batch_save_msa_feat.py` inside `ColabFold/colabfold/` and run following command 

`python batch_save_msa_feat.py --num-models 1 --save-pair-representations --num-recycle 1 --recompile-padding 1 your_input_fasta.fasta target_feature_`

The output of the MSA first row featue will be saved as `target_feature_msa_first_row.npy`

An example of MSA first row feature can be found [here](../Preprocessing/input/4zm2_Bmsa_first_row.npy)
