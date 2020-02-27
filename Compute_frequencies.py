import sys
from DockingPP.core import parse, zParse

import pickle
import argparse

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to compute residue and contact frquencies in a set of docking poses" )
	parser.add_argument("--list", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--input_pdb", metavar = "<dir>", help = "Directory with the starting PDB files", required = True)
	parser.add_argument("--N", metavar = "<int>", help = "Number of poses to treat (default 50)", default = 50, type=int)
	return parser.parse_args()

if __name__ == "__main__":
	ARGS = args_gestion()

	with open(ARGS.list) as f:
		lines=f.readlines()

	nb_prot = 0
	nb_prot_total = len(lines)
	for prot in lines:
		nb_prot += 1
		print(str(nb_prot) + "/" + str(nb_prot_total))
		prot=prot.strip()
		DD=zParse(ARGS.zdock_results + "/" + prot+".zd3.0.2.fg.fixed.out",maxPose=ARGS.N)
		DD.setReceptor(ARGS.input_pdb + "/" + prot+"_r_u.pdb")
		DD.setLigand(ARGS.input_pdb + "/" + prot+"_l_u.pdb")

		DD.ccmap(start=0,stop=ARGS.N)
		[ResStats,ConStats]=DD.getStats
		with open(prot+"_resstats.pkl", 'wb') as f2:
			pickle.dump(ResStats, f2)
		with open(prot+"_constats.pkl", 'wb') as f2:
			pickle.dump(ConStats, f2)




