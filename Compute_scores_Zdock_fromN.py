import sys
from DockingPP.core import parse, zParse

if len(sys.argv) ==0 :
	print("usage : python Compute_score_Zdock.py -l <complexes list> -p <zdock results path> -i <input pdbs path> -o <output dir> -n_stat N_stat [default 500] -n_eval N_eval [default 500]")
	exit()


N_stat=500
N_eval=500

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
    if arg == '-n_stat':
        i=i+1
        N_stat=int(sys.argv[i])
    if arg == '-n_eval':
        i=i+1
        N_eval=int(sys.argv[i])       
    i=i+1


print("will evaluate the first "+str(N_eval)+" in each decoy set, with statistics from the top "+str(N_stat))

with open(my_proteins) as f:
	lines=f.readlines()

nb_prot = 0
nb_prot_total = len(lines)
for prot in lines:
	nb_prot += 1
	print(str(nb_prot) + "/" + str(nb_prot_total))
	prot=prot.strip()
	DD=zParse(my_Zdock_path + "/" + prot+".zd3.0.2.fg.fixed.out",maxPose=N_stat)
	DD.setReceptor(my_input_path + "/" + prot+"_r_u.pdb")
	DD.setLigand(my_input_path + "/" + prot+"_l_u.pdb")
	DD.ccmap(start=0,stop=N_stat)
	rec_residues=DD[1].belongsTo.pdbObjReceptor.getResID
	[newResStats,newConStats]=DD.getStats

	DD2=zParse(my_Zdock_path+ "/" +prot+".zd3.0.2.fg.fixed.out",maxPose=N_eval)
	DD2.setReceptor(my_input_path+prot+"_r_u.pdb")
	DD2.setLigand(my_input_path+prot+"_l_u.pdb")
	DD2.ccmap(start=0,stop=N_eval)
	rec_residues=DD2[1].belongsTo.pdbObjReceptor.getResID

	DD2.all_scores(resStats=newResStats,conStats=newConStats)
	DD2.write_all_scores(filename=results_dir + "/" + prot,resStats=newResStats,conStats=newConStats,maxPose=N_eval) 



