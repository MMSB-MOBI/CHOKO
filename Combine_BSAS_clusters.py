import sys
from DockingPP.core import zParse
from DockingPP.core_clustering import BSAS
from DockingPP.core_scores import countNative
import argparse

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to count the number of successes after rescoring")
	parser.add_argument("-N", metavar = "<int>", help = "Number of zdock scores to keep (default : 6)", default = 6, type=int)
	parser.add_argument("--score", metavar = "<str>", help = "Score type", default = "res_fr_sum")
	parser.add_argument("--list_complex", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--maxD", metavar = "<int>", help = "??", default=3, type=int)
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
		DD=zParse(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out", maxPose = ARGS.max_pose)
		DD.setScores(filename = ARGS.all_scores + "/" + prot + ".tsv")

		# read the RMSD file 
		with open(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out.rmsds") as f:
			lines=f.readlines()

		data=[L.split()[1] for L in lines[0:ARGS.max_pose]]
		# add it into the DD object, pose by pose 
		for i in range(ARGS.max_pose):
			DD.pList[i].set_RMSD(float(data[i]))
		
		DD.scores.setPoses(DD.pList)
		
		native_ranked_poses=[pose for pose in DD.rankedPoses()]
		
		new_ranked_poses=DD.rankedPoses(element=ARGS.score)

		c_clusters1=BSAS(native_ranked_poses, ARGS.maxD, out='dict', stop=ARGS.max_pose)
		NbClus=len(c_clusters1)
		# Get first pose (representative) for each cluster ? 
		my_list1=[c_clusters1[i+1][0] for i in range(NbClus)]

		c_clusters2=BSAS(new_ranked_poses, ARGS.maxD, out='dict', stop=ARGS.max_pose)
		NbClus = len(c_clusters2)
		my_list2=[c_clusters2[i+1][0] for  i in range(NbClus)]

		# First Zdock clusters, then other clusters 
		my_added_poses = [p for p in my_list2 if p not in my_list1[:ARGS.N]][0:(10-ARGS.N)]
		my_list_final=my_list1[:ARGS.N] + my_added_poses
		rmsds=DD.scores.rankedRmsds(my_list_final)
		NB=countNative(rmsds, cutoff=2.5)[10]
		if NB>0:
			NB_SUCCESS+=1

	print(NB_SUCCESS)
