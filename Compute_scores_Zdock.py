import sys
sys.path.append("/Users/jmartin/CHOKO/2020_01_17_DEV_LIB/DockingPP/")
sys.path.append("/Users/jmartin/CHOKO/2020_01_17_DEV_LIB/pyproteinsExt/src/")
from DockingPP.core import parse, zParse

if len(sys.argv) ==0 :
	print("usage : python Compute_score_Zdock.py -l <complexes list> -p <zdock results path> -i <input pdbs path> -o <output dir> [-n N_max  (default 500)]")
	exit()


N_max=500

i=1
while i < len(sys.argv):
    arg=sys.argv[i]
    if arg == '-l':
        i=i+1
        my_proteins=sys.argv[i]
    if arg == '-p':
        i=i+1
        my_Zdock_path=sys.argv[i]
    if arg == '-i':
        i=i+1
        my_input_path=sys.argv[i]
    if arg == '-o':
        i=i+1
        results_dir=sys.argv[i].rstrip("/")
    if arg == '-n':
        i=i+1
        N_max=int(sys.argv[i])
    i=i+1

#my_Zdock_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/results/"
#my_input_path="/Users/jmartin/CHOKO/DATA/ZDOCK_3.0.2/decoys_bm4_zd3.0.2_6deg_fixed/input_pdbs/"

print("will evaluate the first "+str(N_max)+" in each decoy set")

with open(my_proteins) as f:
	lines=f.readlines()

nb_prot = 0
nb_prot_total = len(lines)
for prot in lines:
	nb_prot += 1
	print(str(nb_prot) + "/" + str(nb_prot_total))
	prot=prot.strip()
	DD=zParse(my_Zdock_path + "/" + prot+".zd3.0.2.fg.fixed.out",maxPose=N_max)
	DD.setReceptor(my_input_path + "/" + prot+"_r_u.pdb")
	DD.setLigand(my_input_path + "/" + prot+"_l_u.pdb")
	DD.ccmap(start=0,stop=N_max)
	rec_residues=DD[1].belongsTo.pdbObjReceptor.getResID
	DD.write_all_scores(filename=results_dir + "/" + prot) 



