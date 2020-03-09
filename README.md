# Rescoring ensembles of protein-protein docking poses using consensus approaches
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
TBD: Explain the principle of consensus-based rescoring

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
  *Python (3.7)
  *DockingPP (https://github.com/MMSB-MOBI/DockingPP): implements consensus rescoring functions
  *pyProteinsExt (https://github.com/MMSB-MOBI/pyproteinsExt): implements functions for protein structure manipulation
  *ccmap (https://github.com/MMSB-MOBI/ccmap): code in C to compute contact maps based on the neighbour cell algorithm

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

### Install DockingPP and its dependencies
Clone the repository and go inside
``` 
git clone https://github.com/MMSB-MOBI/DockingPP
cd DockingPP
```

Install python dependencies (including pyProteinsExt)
```
pip install -r requirements.txt
```

Add DockingPP to your PYTHONPATH

```
export PYTHONPATH=$PYTHONPATH:DOCKINGPP_LOCAL_PATH

```

## Method overview



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
