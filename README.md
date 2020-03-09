# Rescoring ensembles of protein-protein docking poses using consensus approaches
TBD: Add an image

TBD: Add a link to the preprint paper


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

Consensus rescoring has been tested on both Linux (TBD give specification of Cecile's machine) and Mac OS environments (macOS Mojave, processor 3.1 GHz Intel Core i7, 16GB memory). To reproduce the experiments in the paper, the data set will consume approximately 940 Megabytes.

All the computations are run on a data set of decoys of 90 protein-protein complexes. The precomputation of contact and residue frequencies takes about 2 minutes for N=50 docking poses, up to 40 minutes for N=2000 docking poses.
The computation of docking pose scores takes about 40 minutes for N=2000 docking poses.
The evaluation steps take several minutes.
Overall, there is no need for a distributed cluster to reproduce the data shown here.

## Software prerequisites
Consensus Rescoring is written in python 3 and relies on other software/libraries written by us, which themselves have dependencies.
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

### Install DockingPP and its dependencies (including pyProteinsExt)
``` 
git clone https://github.com/MMSB-MOBI/DockingPP
cd DockingPP
pip install -r requirements.txt
```

Add DockingPP to your PYTHONPATH

```
export PYTHONPATH=$PYTHONPATH:DOCKINGPP_LOCAL_PATH

```
### Clone Consensus Rescoring 
Clone Consensus Rescoring to a local directory
```
git clone https://github.com/MMSB-MOBI/Consensus_rescoring
cd Consensus_rescoring
```

## Method overview

Explain the four different rescoring functions 

## Application

  ### ZDOCK data retrieval and pre-processing
https://zlab.umassmed.edu/zdock/decoys.shtml  
ZDOCK 3.0.2, 6 degree sampling, fixed receptor
  
  
  ### Precomputation of residue/contact scores
  ### Precomputation of consensus scores of docking poses
  ### Evaluation of Different Consensus-Based Rescoring Functions
  ### Combination with ZDOCK Native Scoring Function
  ### Combination of Clusters
  
  
## License

??

## Reference
When accepted




## Reproduce results from the article 
See Reproduce_published_results2020.py 
