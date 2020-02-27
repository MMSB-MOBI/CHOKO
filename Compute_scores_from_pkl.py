import sys
import pickle
from DockingPP.core import parse, zParse
import argparse

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to compute residue and contact frquencies in a set of docking poses" )
	parser.add_argument("--list", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--input_pdb", metavar = "<dir>", help = "Directory with the starting PDB files", required = True)
	parser.add_argument("--N", metavar = "<int>", help = "Number of poses to treat (default 2000)", default = 2000, type=int)
	parser.add_argument("--freq_dir", metavar = "<dir>", help = "Directory where the frequencies are stored", required = True)

	return parser.parse_args()

if __name__ == "__main__":
	ARGS = args_gestion()


with open(ARGS.list) as f:
	lines=f.readlines()

	with open(ARGS.list) as f:
		lines=f.readlines()

	for prot in lines:
		prot=prot.strip()
		with open (ARGS.freq_dir + "/" + prot+"_resstats.pkl", 'rb') as f2:
			newResStats=pickle.load(f2)
		with open (ARGS.freq_dir + "/" + prot+"_constats.pkl", 'rb') as f2:
			newConStats=pickle.load(f2)
		DD2=zParse(ARGS.zdock_results+ "/" +prot+".zd3.0.2.fg.fixed.out",maxPose=ARGS.N)
		DD2.setReceptor(ARGS.input_pdb+prot+"_r_u.pdb")
		DD2.setLigand(ARGS.input_pdb+prot+"_l_u.pdb")
		DD2.ccmap(start=0,stop=ARGS.N)
		DD2.all_scores(resStats=newResStats,conStats=newConStats)
		DD2.write_all_scores(filename= prot,resStats=newResStats,conStats=newConStats,maxPose=ARGS.N) 



