# EquiPNAS: Improved Protein-nucleic Acid Binding Site Prediction Using Pretrained Protein Language Model and Equivariant Deep Graph Learning

by Rahmatullah Roche, Bernard Moussad, Md Hossain Shuvo, Sumit Tarafder, and Debswapna Bhattacharya

[[bioRxiv](https://www.biorxiv.org/content/...)] [[pdf](https://www.biorxiv.org/content/....full.pdf)]

Codebase for our Improved protein-nucleic binding site prediction appraoch, EquiPNAS.

![Workflow](./EquiPNAS.png)

## Installation

1.) We recommend conda virtual environment to install dependencies for EquiPNAS. The following command will create a virtual environment named 'EquiPNAS'

`conda env create -f EquiPNAS_environment.yml`

2.) Then activate the virtual environment

`conda activate EquiPNAS`

3.) Download the trained models
	- for protein-DNA binding site prediction, download EquiPNAS-DNA model [here](models/EquiPNAS-DNA/)
	- for protein-RNA binding site prediction, download EquiPNAS-RNA model [here](models/EquiPNAS-RNA/)


That's it! EquiPNAS is ready to be used.
