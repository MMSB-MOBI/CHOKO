# CReDock: Consensus Rescoring of Protein-Protein Docking Ensembles
TBD: Add an image !!!!!

TBD: Add a link to the preprint paper

TBD: find a name for the package !!
CReDock ?
DRAKAR ?
CHOKO ?

## Content
- [Description](#description)
- [System and hardware requirements](#system-and-hardware-requirements)
- [Software prerequisites](#software-prerequisites)
- [Installation](#Installation)
- [Method overview](#Method-overview)
- [Application](#Application)
  - ZDOCK data retrieval and pre-processing
  - Precomputation of residue/contact scores
  - Precomputation of consensus scores of docking poses
  - Evaluation of Different Consensus-Based Rescoring Functions
  - Combination with ZDOCK Native Scoring Function
  - Combination of Clusters
- [License](#License)
- [Reference](#Reference)

## Description
CReDock aims at rescoring set of protein-protein docking solutions based on consensus.

The principle of consensus rescoring is to identify, among a (large) set of solutions generated by a docking software, the solutions that are best representative of the whole set. In practice, CReDock computes statistics on interface contacts or interface residues in the set of docking solutions, and uses these statistics to build a score for each docking pose.

In practice, CReDock operates on data sets produced by a docking software, in this case the well-known ZDOCK software (Pierce BG, Hourai Y, Weng Z. Accelerating Protein Docking in ZDOCK Using an Advanced 3D Convolution Library. PLOS ONE 2011;6(9):e24657). Hence we do not provide tools for docking, we only consider the post-processing step.

In addition, we do not provide here physics-based or evolutionnary-based evaluation of docking poses.


This repository should closely reproduce the experiments of:
Add reference of paper upon publication acceptance


## System and hardware requirements

CReDock has been tested on both Linux (TBD give specification of Cecile's machine) and Mac OS environments (macOS Mojave, processor 3.1 GHz Intel Core i7, 16GB memory). To reproduce the experiments in the paper, the data set will consume approximately 940 Megabytes.

All the computations are run on a data set of decoys of 90 protein-protein complexes. The precomputation of contact and residue frequencies takes about 2 minutes for N=50 docking poses, up to 40 minutes for N=2000 docking poses.
The computation of docking pose scores takes about 40 minutes for N=2000 docking poses.
The evaluation steps take several minutes.
Overall, there is no need for a distributed cluster to reproduce the data shown here.

## Software prerequisites
CReDock is written in python 3 and relies on other software/libraries written by us, which themselves have dependencies.
The following is required:
  - Python (3.7)
  - DockingPP (https://github.com/MMSB-MOBI/DockingPP): implements consensus rescoring functions
  - pyProteinsExt (https://github.com/MMSB-MOBI/pyproteinsExt): implements functions for protein structure manipulation
  - ccmap (https://github.com/MMSB-MOBI/ccmap): code in C to compute contact maps based on the neighbour cell algorithm

## Installation 

### Install Python 3
Our code has been tested with python 3.7.4. Feel free to test other python3 versions and give us feedback. 
A simple solution is to create a new conda environment with python 3.
```
conda create -n consensus_rescoring python=3.7.4
conda activate consensus_rescoring
```
Each time you want to work with consensus_rescoring you will have to activate the environment. 

### Compile and install ccmap
```
git clone https://github.com/MMSB-MOBI/ccmap
cd ccmap
python setup.py build
python setup.py install
```
Or 
```
pip install ccmap
```

### Install DockingPP and its dependencies (including pyProteinsExt)
``` 
git clone https://github.com/MMSB-MOBI/DockingPP
cd DockingPP
pip install -r requirements.txt
cd ..
```

Add DockingPP to your PYTHONPATH

```
export PYTHONPATH=$PYTHONPATH:$PWD/DockingPP/
```
### Clone CReDock
Clone CReDock to a local directory
```
git clone https://github.com/MMSB-MOBI/Consensus_rescoring
export SRC_DIR=$PWD/Consensus_rescoring
```

## Method overview
We implemented four different scoring functions, based on the frequencies of interface contacts or interface residue seen in the set of docking solutions, defined by a distance between heavy atoms lower than 5 &Aring;.

The principle is to screen the set of docking poses to compute the frequencies of interface contacts or interface residues.
These frequencies are then used to attribute a score for each docking pose, according to the contacts or residues observed at the interface.

The four scoring functions are :
 1. Contact_Average score: the score of a docking pose is the sum of the contact relative frequencies, divided by the number of contacts at the interface. Please note that this is identical to the CONSRANK scoring scheme introduced in (Oliva R, Vangone A, Cavallo L. Ranking multiple docking solutions based on the conservation of inter-residue contacts. Proteins: Structure, Function, and Bioinformatics. 2013;81: 1571–1584. doi:10.1002/prot.24314).
 
 2. Contact_Sum score: the score of a docking pose is the sum of the contact relative frequencies. 
 3. Residue_Average: the score of a docking pose is the sum of the residue relative frequencies, divided by the number of residues at the interface.
 4. Residue_Sum: the score of a docking pose is the sum of the residue relative frequencies.

## Application

  ### ZDOCK data retrieval and pre-processing
  Retrieve the ZDOCK benchmark set (ZDOCK 3.0.2, 6 degree sampling, fixed receptor format):
  ```
  curl -O  https://zlab.umassmed.edu/zdock/decoys_bm4_zd3.0.2_6deg_fixed.tar.gz 
  ```
  Reformat the input PDB files to have 55 character long lines
  ```
  $SRC_DIR/Reformat_PDB_files.sh
  export ZDOCK_DIR=$PWD/decoys_bm4_zd3.0.2_6deg_fixed/
  ```

  ### Computation of residue/contact scores
Compute the frequencies of interface contacts and interface residues, and store them in pickled ojects:
```
source $SRC_DIR/Compute_frequencies.sh
```
This script will create four directories:
1. Freq_top50: frequencies computed from the top 50 ZDOCK poses for each complex, requires about 2 minutes, size 4.0 MB,
2. Freq_top100: frequencies computed from the top 100 ZDOCK poses for each complex, requires about 4 minutes, size 5.5 MB,
3. Freq_top1000: frequencies computed from the top 1000 ZDOCK poses for each complex, requires about 18 minutes, size 14 MB,
4. Freq_top2000: frequencies computed from the top 2000 ZDOCK poses for each complex, requires about 38 minutes, size 19MB.


### Computation of consensus scores of docking poses
Compute the consensus scores of the first 2000 ZDOCK poses using :
```
source $SRC_DIR/Compute_scores.sh
```
This script will create four directories:
1. Scores_Freq_top50: scores of the first 2000 ZDOCK poses, using frequencies in Freq_top50,
2. Scores_Freq_top100: scores of the first 2000 ZDOCK poses, using frequencies  in Freq_top100,
3. Scores_Freq_top1000: scores of the first 2000 ZDOCK poses, using frequencies  in Freq_top1000, 
4. Scores_Freq_top2000: scores of the first 2000 ZDOCK poses, using frequencies  in Freq_top2000, 

Each directory creation will require about 36 minutes, and consume 27.0MB of storage.


### Evaluation of Different Consensus-Based Rescoring Functions
Compute the number of successes using each scoring function:
```
source $SRC_DIR/Evaluate_scoring_functions.sh
```
Requires about 5 minutes.

This script will create one file with the results presented in Figure 1 of the article:
```
NB_success_separate_scoring_functions.txt
```

### Combination of Consensus Scores with ZDOCK Native Scoring Function
Compute the number of successes using the combination of consensus based scoring functions and the ZDOCK native scoring function:
```
source $SRC_DIR/Evaluate_pose_combination.sh
```
Requires about 5 minutes.

This script will create one file with the results presented in Figure 2 of the article:
```
NB_success_combination.txt
```


To get the number of near-native docking hits for each protein complex,run the python script with the --verbose True option:
```
python $SRC_DIR/Compute_NB_success.py --score residue_sum --list $SRC_DIR/listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores Scores_Freq_top100/  --rmsd 2.5 --N_native 7 --verbose True 
```


To get access to the selected poses for one particular complex, run the python with the --verbose Ultra option:
```
echo "1E6E" > list.temp
python $SRC_DIR/Compute_NB_success.py --score residue_sum --list list.temp  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores Scores_Freq_top100/  --rmsd 2.5 --N_native 7 --verbose Ultra 
```



### Combination of Clusters
  Compute the number of successes using the BSAS clustering, and a combination of consensus based scoring functions and the ZDOCK native scoring function:
```
source $SRC_DIR/Evaluate_cluster_combination.sh
```
Requires 7 minutes.

This script will create one file with the results presented in Figure 3 of the article:
```
NB_success_cluster_combination.txt
```

To retrieve the selected pose shown in Figure 4, run the python script with the --verbose Ultra option:
```
echo "1AVX
1EAW
1XQS
1E6E" > list.txt

python $SRC_DIR/Combine_BSAS_clusters_Nrange.py --N_native 5 --verbose Ultra --score contact_sum --maxD 8 --list list.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores Scores_Freq_top1000/  --rmsd 2.5 > poses_figure4.txt
```


## License

??

## Reference
When accepted


