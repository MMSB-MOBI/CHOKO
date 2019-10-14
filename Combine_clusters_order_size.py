import sys
sys.path.append("/Users/jmartin/STAGE_JULIA/2019_07_18_DEMO/DockingPP")
from dockingPP import parse, zParse
from src.core_scores import Scores, countNative, eval_natives
from src.core_clustering import rankCluster as rC, sortCluster, birchCluster



N=6
score_name='res_fr_sum'


if len(sys.argv)==1:
    print('%s: a programm to count the number of successes after rescoring  and clustering '%sys.argv[0])
    print('usage: %s -N NB_Zdock -score score_name'%sys.argv[0])
    sys.exit(1)

i=1
while i < len(sys.argv):
    arg=sys.argv[i]
    if arg == '-N':
        i=i+1
        N=int(sys.argv[i])
    if arg == '-score':
        i=i+1
        score_name=sys.argv[i]  
    i=i+1

NB_SUCCESS=0


my_Zdock_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/results/"
my_input_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/input_pdbs/"

with open("list.txt") as f:
	lines=f.readlines()


for prot in lines:
	prot=prot.strip()
	
	# read the docking output file 
	DD=zParse(my_Zdock_path+prot+".zd3.0.2.fg.fixed.out",maxPose=500)
	DD.setScores(filename="all_scores"+prot+".tsv")

	# read the RMSD file 
	with open(my_Zdock_path+prot+".zd3.0.2.fg.fixed.out.rmsds") as f:
		lines=f.readlines()
	data=[L.split()[1] for L in lines[0:500]]
	# add it into the DD object, pose by pose 
	for i in range(500):
		DD.pList[i].set_RMSD(float(data[i]))

	
	DD.scores.setPoses(DD.pList)
	
	# cluster the poses using native ranks :
	native_ranked_poses=[i+1 for  i in range(500)]
	native_ranked_indexes=[i-1 for i in native_ranked_poses]

	new_ranked_poses=DD.scores.rankedPoses(element=score_name)
	new_ranked_indexes=[i-1 for i in new_ranked_poses]

	# Ici: il faut donner des INDICES correspondants aux poses dans le nouvel ordre
	c_clusters1=rC(DD.pList,native_ranked_indexes,5, out='dict', stop=500)

	# on range les clusters dans l'ordre de taille décroissant 
	cluster_sizes1=[len(c_clusters1[c]) for c in c_clusters1]
	sorted_indexes1=sorted(range(len(cluster_sizes1)), key=lambda k: cluster_sizes1[k],reverse=True)
    # Ici, il faut récupérer les poses représentatives de ces clusters 
    # ATTENTION: sorted_indexes sont des indexes (0 à N-1) alors que c_clusters1 a comme clé des numéros de clusters (1 à N)
	my_list1=[c_clusters1[i+1][0].id for i in sorted_indexes1][:N]
   


	c_clusters2=rC(DD.pList,new_ranked_indexes,5, out='dict', stop=500)
	cluster_sizes2=[len(c_clusters2[c]) for c in c_clusters2]
	sorted_indexes2=sorted(range(len(cluster_sizes2)), key=lambda k: cluster_sizes2[k],reverse=True)
	my_list2=[c_clusters2[i+1][0].id for i in sorted_indexes2]
   
	my_added_poses=[p for p in my_list2 if p not in my_list1][0:(10-N)]
	my_list_final=my_list1+my_added_poses

	my_indexes=[i-1 for i in my_list_final]
	rmsds=DD.scores.rankedRmsds(my_indexes)

	NB=countNative(rmsds, cutoff=2.5)[10]

	if NB>0:
		NB_SUCCESS+=1



print(NB_SUCCESS)
