import sys
from DockingPP.core import parse, zParse

if len(sys.argv) != 5:
	print("usage : python Compute_score_Zdock.py <complexes list> <zdock results path> <input pdbs path> <results dir>")
	exit()

#my_Zdock_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/results/"
my_Zdock_path = sys.argv[2]
#my_input_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/input_pdbs/"
my_input_path = sys.argv[3]
my_proteins = sys.argv[1]
results_dir = sys.argv[4].rstrip("/")

with open(my_proteins) as f:
	lines=f.readlines()

nb_prot = 0
nb_prot_total = len(lines)
for prot in lines:
	nb_prot += 1
	print(str(nb_prot) + "/" + str(nb_prot_total))
	prot=prot.strip()
	DD=zParse(my_Zdock_path + "/" + prot+".zd3.0.2.fg.fixed.out",maxPose=500)
	DD.setReceptor(my_input_path + "/" + prot+"_r_u.pdb")
	DD.setLigand(my_input_path + "/" + prot+"_l_u.pdb")
	DD.ccmap(start=0,stop=500)
	rec_residues=DD[1].belongsTo.pdbObjReceptor.getResID
	DD.write_all_scores(filename=results_dir + "/" + prot) 
	# Ici on peut assigner des statistiques extérieures 
	# qu'on aura récupérer par DD.getStats()
	# DD.all_scores(resStats= conStats=)



