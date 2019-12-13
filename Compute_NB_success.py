import sys
from DockingPP.core import zParse
import argparse
from DockingPP.core_scores import countNative

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to count the number of successes after rescoring")
	parser.add_argument("-N", metavar = "<int>", help = "Number of zdock scores to keep (default : 6)", default = 6, type=int)
	parser.add_argument("--score", metavar = "<str>", help = "Score type", default = "res_fr_sum")
	parser.add_argument("--list_complex", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--max_pose", metavar = "<int>", help = "Number of poses to keep (default: 500)", default = 500, type=int)
	parser.add_argument("--all_scores", metavar = "<dir>", help = "Directory with all scores computed", required = True)

	return parser.parse_args()

if __name__ == "__main__":
	ARGS = args_gestion()
	NB_SUCCESS = 0
	with open(ARGS.list_complex) as f:
		for prot in f: 
			prot=prot.strip()
			#print(prot)
			# read the docking output file 
			DD = zParse(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out", maxPose = ARGS.max_pose)
			DD.setScores(filename=ARGS.all_scores + "/" + prot + ".tsv")
			# read the RMSD file 
			with open(ARGS.zdock_results + "/" + prot +".zd3.0.2.fg.fixed.out.rmsds") as f:
				lines=f.readlines()
			data=[L.split()[1] for L in lines[0:500]]
			# add it into the DD object, pose by pose 
			for i in range(ARGS.max_pose):
				DD.pList[i].set_RMSD(float(data[i]))

			# A tester : 
			#DD.get_rmsd(filename=)
			
			# Evaluation
			# get the N first according to the native scoring function
			my_list1=[pose for pose in DD.rankedPoses()[:ARGS.N-1]]
			#show there rmsd 
			#my_indexes=[i-1 for i in my_list1]
			#print(DD.scores.rankedRmsds(my_indexes))

			# select the N=10 first according to score
			my_list2=DD.rankedPoses(element=ARGS.score)[:10]

			my_added_poses=[p for p in my_list2 if p not in my_list1][0:(10-ARGS.N)]
			my_list_final=my_list1 + my_added_poses
			rmsds=DD.scores.rankedRmsds(my_list_final)

			NB=countNative(rmsds, cutoff=2.5)[10]

			if NB>0:
				NB_SUCCESS+=1

	print(NB_SUCCESS)
