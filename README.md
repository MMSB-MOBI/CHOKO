# CHOKO: Consensus rescoring of High-throughput protein-protein dOcKing pOses


## Content
- [Description](#description)
- [System and hardware requirements](#system-and-hardware-requirements)
- [Software prerequisites](#software-prerequisites)
- [Installation](#Installation)
- [Method overview](#Method-overview)
- [Application](#Application)
- [Reference](#Reference)

## Description
CHOKO aims at rescoring large set of protein-protein docking solutions based on consensus.

This repository should reproduce the experiments of:
Rescoring ensembles of protein-protein docking poses using consensus approaches
Guillaume Launay, Masahito Ohue, Julia Prieto Santero, Yuri Matsuzaki, Cécile Hilpert, Nobuyuki Uchikoga, Takanori Hayashi, Juliette Martin.
doi: https://doi.org/10.1101/2020.04.24.059469 


The consensus rescoring of protein-protein docking poses has been introduced by Oliva et al in 2013
(Oliva R, Vangone A, Cavallo L. Ranking multiple docking solutions based on the conservation of inter-residue contacts. Proteins: Structure, Function, and Bioinformatics. 2013;81: 1571-1584. doi:10.1002/prot.24314) and successfully applied then (Vangone A, Cavallo L, Oliva R. Using a consensus approach based on the conservation of inter-residue contacts to rank CAPRI models. Proteins: Structure, Function, and Bioinformatics 2013;81(12):2210-2220, Oliva R, Chermak E, Cavallo L. Analysis and Ranking of Protein-Protein Docking Models Using Inter-Residue Contacts and Inter-Molecular Contact Maps. Molecules 2015;20(7):12045-12060,  Chermak E, Donato RD, Lensink MF, Petta A, Serra L, Scarano V, Cavallo L, Oliva R. Introducing a Clustering Step in a Consensus Approach for the Scoring of Protein-Protein Docking Models. PLOS ONE 2016;11(11):e0166460).
 
CHOKO computes statistics on interface contacts or interface residues in the set of docking solutions, and uses these statistics to build a score for each docking pose.
Four scores are implemented: two scores proposed by Oliva et al in the CONSRANK method (Oliva R, Vangone A, Cavallo L. Ranking multiple docking solutions based on the conservation of inter-residue contacts. Proteins: Structure, Function, and Bioinformatics. 2013;81: 1571–1584. doi:10.1002/prot.24314), and two variations on it, based on interface residues.

CHOKO operates on data sets produced by a docking software, in this case the well-known ZDOCK software (Pierce BG, Hourai Y, Weng Z. Accelerating Protein Docking in ZDOCK Using an Advanced 3D Convolution Library. PLOS ONE 2011;6(9):e24657). Hence we do not provide tools for docking, we only consider the post-processing step.
In addition, we do not provide here physics-based or evolutionnary-based evaluation of docking poses.

CHOKO allows to test different scores, with different ensembles of solution for statistics and evaluation. It operates directly on ZDOCK output files, and allows to treat thousands of docking poses.
It requires scripting (see below).

If you wish to apply the CONSRANK score on a set of PDB files, you should use the CONSRANK webserver:
https://www.molnac.unisa.it/BioTools/consrank/
(Chermak E, Petta A, Serra L, Vangone A, Scarano V, Cavallo L, Oliva R. CONSRANK: a server for the analysis, comparison and ranking of docking models based on inter-residue contacts. Bioinformatics 2015;31(9):1481–1483.)

The structural clustering of the docking poses is done with the Basic Sequential Algorithmic Scheme (BSAS) (Koutroumbas K, Theodoridis S. Pattern Recognition. Amsterdam: Academic Press; 2008) as in (Jiménez-García B, Roel-Touris J, Romero-Durana M, Vidal M, Jiménez-González D, Fernández-Recio J. LightDock: a new multi-scale approach to protein–protein dock).

## System and hardware requirements

CHOKO has been tested on both Linux and Mac OS environments (macOS Mojave, processor 3.1 GHz Intel Core i7, 16GB memory). To reproduce the experiments in the paper, the data set will consume approximately 880 Megabytes.

All the computations are run on a data set of decoys of 90 protein-protein complexes. The computation of contact and residue frequencies and rescoring of 2000 poses takes about 3 minutes for the 90 complexes.
Overall, there is no need for a distributed cluster to reproduce the data shown here.

## Software prerequisites
CHOKO is written in python 3 and relies on other software/libraries written by us, which themselves have dependencies.
The following is required:
  - Python (3.8)
  - DockingPP (https://github.com/MMSB-MOBI/DockingPP): implements consensus rescoring functions
  - pyProteinsExt (https://github.com/MMSB-MOBI/pyproteinsExt): implements functions for protein structure manipulation
  - ccmap (https://github.com/MMSB-MOBI/ccmap): code in C to compute contact maps based on the neighbour cell algorithm

## Installation 

### Install Python 3
A simple solution is to create a new conda environment with python 3.8
```
conda create -n choko python=3.8
conda activate choko
```
Each time you want to work with choko you will have to activate the environment. 

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

### Install DockingPP and its dependencies
``` 
git clone https://github.com/MMSB-MOBI/DockingPP
cd DockingPP
pip install -r requirements.txt
cd ..
```

Add DockingPP to your PYTHONPATH

```
export PYTHONPATH=$PYTHONPATH:$PWD/DockingPP/src/
```
### Clone CHOKO
Clone CHOKO to a local directory
```
git clone https://github.com/MMSB-MOBI/CHOKO
export SRC_DIR=$PWD/CHOKO
```

## Method overview
We implemented four different scoring functions, based on the frequencies of interface contacts or interface residue seen in the set of docking solutions, defined by a distance between heavy atoms lower than 5 &Aring;.

The principle is to screen the set of docking poses to compute the frequencies of interface contacts or interface residues.
These frequencies are then used to attribute a score for each docking pose, according to the contacts or residues observed at the interface.

The four scoring functions are :
 1. CONSRANK: the score of a docking pose is the sum of the contact relative frequencies, divided by the number of contacts at the interface. This is equation (3) in  Oliva R, Vangone A, Cavallo L. Ranking multiple docking solutions based on the conservation of inter-residue contacts. Proteins: Structure, Function, and Bioinformatics. 2013;81: 1571-1584. doi:10.1002/prot.24314.
 
 2. CONSRANK_U: the score of a docking pose is the sum of the contact relative frequencies. This is equation (2) in  Oliva R, Vangone A, Cavallo L. Ranking multiple docking solutions based on the conservation of inter-residue contacts. Proteins: Structure, Function, and Bioinformatics. 2013;81: 1571-1584. doi:10.1002/prot.24314.
 3. Residue_Average: the score of a docking pose is the sum of the residue relative frequencies, divided by the number of residues at the interface.
 4. Residue_Sum: the score of a docking pose is the sum of the residue relative frequencies.

## Application

  ### 0. ZDOCK data retrieval and pre-processing
  Retrieve the ZDOCK benchmark set (ZDOCK 3.0.2, 6 degree sampling, fixed receptor format):
  ```
  curl -O  https://zlab.umassmed.edu/zdock/decoys_bm4_zd3.0.2_6deg_fixed.tar.gz 
  ```
  Reformat the input PDB files to have 55 character long lines
  ```
  $SRC_DIR/Reformat_PDB_files.sh
  export ZDOCK_DIR=$PWD/decoys_bm4_zd3.0.2_6deg_fixed/
  ```

### 1. Rescoring of the first 2,000 poses

Compute the frequencies of interface contacts and interface residues, and use them to rescore the first 2,000 poses:
```
source $SRC_DIR/Compute_scores.sh
```

This script will create a main directory SCORES, with four subdirectories:
1. SCORES/Freq_top50: scores of the first 2000 ZDOCK poses, using frequencies computed from the top 50 poses, 
2. SCORES/Freq_top100: scores of the first 2000 ZDOCK poses, using frequencies computed from the top 100 poses, 
3. SCORES/Freq_top1000: scores of the first 2000 ZDOCK poses, using frequencies computed from the top 1000 poses, 
4. SCORES/Freq_top2000: scores of the first 2000 ZDOCK poses, using frequencies computed from the top 2000 poses. 

Each directory creation will require about 3 minutes, and consume 13.0MB of storage.


### 2. Evaluation of Different Consensus-Based Rescoring Functions
Compute the number of successes using each scoring function:
```
source $SRC_DIR/Evaluate_scoring_functions.sh
```
Requires about 4 minutes.

This script will create one file with the results presented in Figure 1 of the article:
```
NB_success_separate_scoring_functions.txt
```
See in the TEST_DATA directory.

### 3. Combination of Consensus Scores with ZDOCK Native Scoring Function
Compute the number of successes using the combination of consensus based scoring functions and the ZDOCK native scoring function:
```
source $SRC_DIR/Evaluate_pose_combination.sh
```
Requires about 4 minutes.

This script will create one file with the results presented in Figure 2 of the article:
```
NB_success_combination.txt
```
See in the TEST_DATA directory

To get the number of near-native docking hits for each protein complex,run the python script with the --verbose True option:
```
python $SRC_DIR/Compute_NB_success.py --score residue_sum --list $SRC_DIR/listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --score_dir SCORES/Freq_top2000/  --rmsd 2.5 --N_native 6 --verbose True > verbose_output_NB_success_residue_sum_Freq_top2000_N6.txt
```


To get access to the selected poses for one particular complex, run the python with the --verbose Ultra option:
```
echo "1E6E" > list.temp
python $SRC_DIR/Compute_NB_success.py --score residue_sum --list list.temp  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --score_dir SCORES/Freq_top2000/  --rmsd 2.5 --N_native 6 --verbose Ultra > ultra_verbose_output_1E6E_residue_sum_Freq_top2000_N6.txt
```



### 4. Combination of Clusters
  Compute the number of successes using the BSAS clustering, and a combination of consensus based scoring functions and the ZDOCK native scoring function:
```
source $SRC_DIR/Evaluate_cluster_combination.sh
```
Requires 7 minutes.

This script will create one file with the results presented in Figure 3 of the article:
```
NB_success_cluster_combination.txt
```
See in the TEST_DATA directory.

To retrieve the selected pose shown in Figure 4, run the python script with the --verbose Ultra option:
```
echo "1AVX
1EAW
1XQS
1E6E" > list.txt

python $SRC_DIR/Combine_BSAS_clusters_Nrange.py --N_native 5 --verbose Ultra --score CONSRANK_U --maxD 8 --list list.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --score_dir SCORES/Freq_top1000/  --rmsd 2.5 > poses_figure4.txt
```



## Reference
Rescoring ensembles of protein-protein docking poses using consensus approaches,
Guillaume Launay, Masahito Ohue, Julia Prieto Santero, Yuri Matsuzaki, Cécile Hilpert, Nobuyuki Uchikoga, Takanori Hayashi, Juliette Martin.

doi: https://doi.org/10.1101/2020.04.24.059469 


https://biorxiv.org/cgi/content/short/2020.04.24.059469v1



