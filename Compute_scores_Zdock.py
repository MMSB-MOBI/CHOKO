import sys
sys.path.append("/Users/jmartin/STAGE_JULIA/2019_07_18_DEMO/DockingPP")
from dockingPP import parse, zParse
from src.core_scores import Scores, countNative, eval_natives
from src.core_clustering import rankCluster as rC, sortCluster, birchCluster

my_Zdock_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/results/"
my_input_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/input_pdbs/"

with open("list.txt") as f:
	lines=f.readlines()


for prot in lines:
	prot=prot.strip()
	print(prot)
	DD=zParse(my_Zdock_path+prot+".zd3.0.2.fg.fixed.out",maxPose=500)
	DD.setReceptor(my_input_path+prot+"_r_u.pdb")
	DD.setLigand(my_input_path+prot+"_l_u.pdb")
	DD.ccmap(start=0,stop=500,pSize=2)
	DD.write_all_scores(filename="all_scores"+prot) 
	# Ici on peut assigner des statistiques extérieures 
	# qu'on aura récupérer par DD.getStats()
	# DD.all_scores(resStats= conStats=)



