import sys

from DockingPP.core import zParse
from DockingPP.core_clustering import BSAS
from DockingPP.core_scores import countNative
import argparse

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to count the number of successes after rescoring and clustering" )
	parser.add_argument("--N_native", metavar = "<int>", help = "How many poses from the native ranking should we keep. If not specified, varies between 0 and top_N", type=int,required=False,default=-1)
	parser.add_argument("--score", metavar = "<str>", help = "Score type", default = "res_fr_sum")
	parser.add_argument("--list_complex", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--maxD", metavar = "<int>", help = "cutoff for the clustering (default 8)", default=8, type=float)
	parser.add_argument("--max_pose", metavar = "<int>", help = "Number of poses to keep (default: 500)", default = 500, type=int)
	parser.add_argument("--all_scores", metavar = "<dir>", help = "Directory with all scores computed", required = True)
	parser.add_argument("--top_N", metavar = "<int>", help = "topN to consider (default 10)", default = 10, type=int)
	parser.add_argument("--rmsd", metavar = "<float>", help = "RMSD cutoff (default 2.5)", default = 2.5, type=float)
	parser.add_argument("--verbose", metavar = "<dir>", help = "verbose output (deault False)", default="False",required = False)

	return parser.parse_args()


if __name__ == "__main__":
		ARGS = args_gestion()

		Results={}
		NB_SUCCESS = {}

		if ARGS.N_native>0:
			Results[ARGS.N_native]={}
			NB_SUCCESS[ARGS.N_native]=0

		else:
			for n_native in range(ARGS.top_N+1):
				Results[n_native]={}
				NB_SUCCESS[n_native]=0

		with open(ARGS.list_complex) as f:
			for prot in f: 
				prot=prot.strip()
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
		
				# cluster the poses using native ranks :
				native_ranked_poses=[pose for pose in DD.rankedPoses()]
				new_ranked_poses=DD.rankedPoses(element=ARGS.score)
				c_clusters1=BSAS(native_ranked_poses, ARGS.maxD, out='dict', stop=ARGS.max_pose)
				NbClus=len(c_clusters1)
				# Get first pose (representative) for each cluster ? 
				my_list1=[c_clusters1[i+1][0] for i in range(NbClus)]


				c_clusters2=BSAS(new_ranked_poses, ARGS.maxD, out='dict', stop=ARGS.max_pose)
				NbClus = len(c_clusters2)
				my_list2=[c_clusters2[i+1][0] for  i in range(NbClus)]


				for N in range(ARGS.top_N+1):
					# First Zdock clusters, then other clusters 
					my_added_poses=[p for p in my_list2 if p not in my_list1[:N]][0:(ARGS.top_N-N)]
					my_list_final=my_list1[:N]+my_added_poses
					rmsds=DD.scores.rankedRmsds(my_list_final)
					NB=countNative(rmsds, cutoff=ARGS.rmsd)[ARGS.top_N]
					if NB>0:
						NB_SUCCESS[N]+=1

		for N in range(ARGS.top_N):
			print(str(N)+' '+str(NB_SUCCESS[N]))
