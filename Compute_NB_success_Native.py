import sys

from DockingPP.core import zParse
import argparse
from DockingPP.core_scores import countNative

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to count the number of successes with the native scoring function")
	parser.add_argument("--list_complex", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--top_N", metavar = "<int>", help = "topN to consider", default = 10, type=int)
	parser.add_argument("--rmsd", metavar = "<float>", help = "RMSD cutoff", default = 2.5, type=float)
	parser.add_argument("--all_scores", metavar = "<dir>", help = "Directory with all scores computed", required = True)
	parser.add_argument("--verbose", metavar = "<dir>", help = "verbose output", default="False",required = False)

	return parser.parse_args()

if __name__ == "__main__":
	ARGS = args_gestion()
	NB_SUCCESS = 0
	with open(ARGS.list_complex) as f:
		for prot in f: 
			prot=prot.strip()
			# read the docking output file 
			DD = zParse(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out", maxPose = ARGS.top_N)
			DD.setScores(filename=ARGS.all_scores + "/" + prot + ".tsv")
			# read the RMSD file 
			with open(ARGS.zdock_results + "/" + prot +".zd3.0.2.fg.fixed.out.rmsds") as f:
				lines=f.readlines()
				
			data=[L.split()[1] for L in lines[0:ARGS.top_N]]
			# add it into the DD object, pose by pose 
			for i in range(ARGS.top_N):
				DD.pList[i].set_RMSD(float(data[i]))


			# get the N first according to the native scoring function
			my_list1=[pose for pose in DD.rankedPoses(element="original_rank",stop=ARGS.top_N)[:(ARGS.top_N-1)]]
			my_list_final=my_list1
			rmsds=DD.scores.rankedRmsds(my_list_final)

			NB=countNative(rmsds, cutoff=2.5)[10]

			if NB>0:
				NB_SUCCESS+=1
				if ARGS.verbose=="True":
					print(prot+" "+str(NB))
	if ARGS.verbose=="False":
		print(NB_SUCCESS)
