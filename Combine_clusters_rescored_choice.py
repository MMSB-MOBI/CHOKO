import sys
from DockingPP.core import zParse
from DockingPP.core_clustering import BSAS, sortCluster
from DockingPP.core_scores import countNative

import argparse

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to count the number of successes after rescoring")
	parser.add_argument("-N", metavar = "<int>", help = "Number of zdock scores to keep (default : 6)", default = 6, type=int)
	parser.add_argument("--score", metavar = "<str>", help = "Score type", default = "res_fr_sum")
	parser.add_argument("--list_complex", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--maxD", metavar = "<int>", help = "??", default=5, type=int)
	parser.add_argument("--max_pose", metavar = "<int>", help = "Number of poses to keep (default: 500)", default = 500, type=int)
	parser.add_argument("--all_scores", metavar = "<dir>", help = "Directory with all scores computed", required = True)

	return parser.parse_args()


if __name__ == "__main__":

	ARGS = args_gestion()
	NB_SUCCESS=0

	with open(ARGS.list_complex) as f:
		lines=f.readlines()


	for prot in lines:
		prot=prot.strip()
		
		# read the docking output file 
		DD = zParse(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out", maxPose=ARGS.max_pose)
		DD.setScores(filename = ARGS.all_scores + "/" + prot + ".tsv")

		# read the RMSD file 
		with open(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out.rmsds") as f:
			lines=f.readlines()
		data=[L.split()[1] for L in lines[0:ARGS.max_pose]]
		# add it into the DD object, pose by pose 
		for i in range(ARGS.max_pose):
			DD.pList[i].set_RMSD(float(data[i]))

		
		DD.scores.setPoses(DD.pList)
		
		# cluster the poses using native ranks :

		native_ranked_poses = DD.rankedPoses()
		native_ranks = DD.ranks("original_rank")
		new_ranked_poses=DD.rankedPoses(element=ARGS.score)
		new_ranks = DD.ranks(element = ARGS.score)	

		# Ici: il faut donner des poses dans le nouvel ordre (ranked poses) ou bien les indices correspondants (ranked poses -1) ??? 
		c_clusters1=BSAS(native_ranked_poses, ARGS.maxD, out='dict', stop=ARGS.max_pose)
		sor_bclus1=sortCluster(c_clusters1, native_ranks)
		my_list1=[c[0] for c in sor_bclus1][:ARGS.N]

		c_clusters2=BSAS(new_ranked_poses, ARGS.maxD, out='dict', stop=ARGS.max_pose)
		sor_bclus2=sortCluster(c_clusters2, new_ranks)
		my_list2=[c[0] for c in sor_bclus2]

		my_added_poses=[p for p in my_list2 if p not in my_list1][0:(10-ARGS.N)]
		my_list_final=my_list1 + my_added_poses

		rmsds=DD.scores.rankedRmsds(my_list_final)

		NB=countNative(rmsds, cutoff=2.5)[10]

		if NB>0:
			NB_SUCCESS+=1

	print(NB_SUCCESS)
