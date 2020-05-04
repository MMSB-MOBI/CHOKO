import sys
import DockingPP

import pickle
import argparse

def args_gestion():
	parser = argparse.ArgumentParser(description = "A programm to rescore a set of docking poses from residue and contact frequencies" )
	parser.add_argument("--list", metavar = "<file>", help = "List of complex to process", required = True)
	parser.add_argument("--zdock_results", metavar = "<dir>", help = "Directory with zdock results", required = True)
	parser.add_argument("--input_pdb", metavar = "<dir>", help = "Directory with the starting PDB files", required = True)
	parser.add_argument("--N1", metavar = "<int>", help = "Number of poses to consider to compute residue and contact frequencies (default 50)", default = 50, type=int)
	parser.add_argument("--N2", metavar = "<int>", help = "Number of poses to rescore (default 50)", default = 50, type=int)
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
		max_pose=ARGS.N1
		if (ARGS.N2>ARGS.N1):
			max_pose=ARGS.N2
		# load the poses 
		DH=DockingPP.loadZdock(ARGS.zdock_results + "/" + prot+".zd3.0.2.fg.fixed.out",max_pose)
		DH.setReceptor(ARGS.input_pdb + "/" + prot+"_r_u.pdb")
		DH.setLigand(ARGS.input_pdb + "/" + prot+"_l_u.pdb")

		# use 8 threads, and compute contacts for max_pose poses
		DH.computeContactMap(8,max_pose)
		# compte frequencies only for the restricted set of poses 
		DH.computeFrequencies(ARGS.N1)
		# rescore ARGS.N2 poses
		DH.rescorePoses(ARGS.N2, type_score = "all")
		DH.serializeRescoring(prot+".tsv", ["residues_sum", "residues_average", "contacts_sum", "contacts_average"])


