import sys

from DockingPP.core import zParse
import argparse
from DockingPP.core_scores import countNative

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to count the number of successes after rescoring")
	parser.add_argument("--N_native", metavar = "<int>", help = "How many poses from the native ranking should we keep. If not specified, varies between 0 and top_N", type=int,required=False,default=-1)
	parser.add_argument("--score", metavar = "<str>", help = "Score type", default = "res_fr_sum")
	parser.add_argument("--list_complex", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
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
			# read the docking output file 
			DD = zParse(ARGS.zdock_results + "/" + prot + ".zd3.0.2.fg.fixed.out", maxPose = ARGS.max_pose)
			DD.setScores(filename=ARGS.all_scores + "/" + prot + ".tsv")
			# read the RMSD file 
			with open(ARGS.zdock_results + "/" + prot +".zd3.0.2.fg.fixed.out.rmsds") as f:
				lines=f.readlines()
				
			data=[L.split()[1] for L in lines[0:ARGS.max_pose]]
			# add it into the DD object, pose by pose 
			for i in range(ARGS.max_pose):
				DD.pList[i].set_RMSD(float(data[i]))

			# Evaluation
			# get the top_N first according to the native scoring function
			my_list1=[pose for pose in DD.rankedPoses(element="original_rank",stop=ARGS.top_N)]
			# select the top_N first according to the specified score
			my_list2=DD.rankedPoses(element=ARGS.score,stop=ARGS.max_pose)[:ARGS.top_N]

			if ARGS.N_native>0:
				n_native=ARGS.N_native
				# Combine the two lists
				my_initial_list=[]
				if (n_native > 0):
					my_initial_list=my_list1[:n_native]
				# complete poses from list2, up to top_N	
				my_added_poses=[p for p in my_list2 if p not in my_initial_list][0:(ARGS.top_N-n_native)]
				my_list_final=my_initial_list + my_added_poses

				rmsds=DD.scores.rankedRmsds(my_list_final)
				NB=countNative(rmsds, cutoff=ARGS.rmsd)[ARGS.top_N]
				Results[n_native][prot]=NB
				if NB>0:
					NB_SUCCESS[n_native]+=1

			else:
				for n_native in range(ARGS.top_N+1):
					# Combine the two lists
					my_initial_list=[]
					if (n_native > 0):
						my_initial_list=my_list1[:n_native]
					# complete poses from list2, up to top_N	
					my_added_poses=[p for p in my_list2 if p not in my_initial_list][0:(ARGS.top_N-n_native)]
					my_list_final=my_initial_list + my_added_poses

					rmsds=DD.scores.rankedRmsds(my_list_final)
					NB=countNative(rmsds, cutoff=ARGS.rmsd)[ARGS.top_N]
					Results[n_native][prot]=NB
					if NB>0:
						NB_SUCCESS[n_native]+=1

# Verbose Output :
if ARGS.verbose=="True":
	if ARGS.N_native>0:
		n_native=ARGS.N_native
		for prot in Results[n_native].keys():
				if(Results[n_native][prot]>0):
					print(str(n_native)+' '+prot+' '+str(Results[n_native][prot]))
	else:		
		for n_native in range(ARGS.top_N+1):
				for prot in Results[n_native].keys():
					if(Results[n_native][prot]>0):
						print(str(n_native)+' '+prot+' '+str(Results[n_native][prot]))
# Non-verbose output 
else:
	if ARGS.N_native>0:
		n_native=ARGS.N_native
		print(NB_SUCCESS[n_native])
	else:
		for n_native in range(ARGS.top_N+1):
			print(str(n_native)+' '+str(NB_SUCCESS[n_native]))







