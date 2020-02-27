# Install pyProteinsExt
# 

# Install Docking PP
# 

# Install Consensus_Scoring 
# 


WORK_DIR=$PWD
ZDOCK_DIR=$PWD/decoys_bm4_zd3.0.2_6deg_fixed/
SRC_DIR=path_to/Consensus_rescoring/

##### DATA RETRIEVAL ######
echo "#####"

if [ ! -e decoys_bm4_zd3.0.2_6deg_fixed.tar.gz ]
then
echo "Retrieve ZDOCK data" 
curl -O  https://zlab.umassmed.edu/zdock/decoys_bm4_zd3.0.2_6deg_fixed.tar.gz 
tar xzvf decoys_bm4_zd3.0.2_6deg_fixed.tar.gz 
cd decoys_bm4_zd3.0.2_6deg_fixed/input_pdbs/
	# reformat to have a parsable PDB format
	for file in `ls *.pdb.ms `; do cut -c1-55 $file > ${file%%.ms}; done

cd $WORK_DIR
echo " ZDOCK data retrieved"
else 
echo "ZDOCK data already retrieved -> nothing to do "
fi

# make the list of proteins to treat 
if [ ! -e listBM.txt ]
then
awk  '{if($3!="--" && $3<=2000){print $1}}' $ZDOCK_DIR/stats.bm4.zd3.0.2.fg.fixed.txt  > listBM.txt
fi
echo "#####"

####### COMPUTATION OF RESIDUE/CONTACT STATISTICS #######

# It takes 2 minutes with N=50
# It takes 4 minutes with N=100
# It takes 18 minutes with N=1000
# It takes 38 minutes with N=2000 
echo "Pre-compute Residue and Contact Frequencies with frequency set = top50 top100 top1000 top2000"
for N in 50 100 1000 2000 
do

    if [ ! -d Freq_top$N ]
    then
    mkdir Freq_top$N
    fi

cd Freq_top$N  
#python $SRC_DIR/Compute_frequencies.py --list ../listBM.txt --zdock_results $ZDOCK_DIR/results/ --input_pdb $ZDOCK_DIR/input_pdbs/ --N $N
cd ..
done 

echo "#####"
####### COMPUTATION OF CONSENSUs SCORES  #######

# It takes 36 minutes for each value of N
echo "Compute consensus scores for the first 2000 poses"
for N in 50 100 1000 2000 
do
    if [ ! -d Scores_Freq_top$N ]
    then
    mkdir Scores_Freq_top$N
    fi
cd Scores_Freq_top$N

    for protein in `cat ../listBM.txt `
    do
    echo $protein > list.temp
        if [ ! -e $WORK_DIR/Scores_Freq_top$N/$protein.tsv ]
        then
        echo $protein 
        python $SRC_DIR/Compute_scores_from_pkl.py --list list.temp --zdock_results $ZDOCK_DIR/results/ --input_pdb $ZDOCK_DIR/input_pdbs/ --N 2000 --freq_dir $WORK_DIR/Freq_top$N
        fi
    done
cd ..
done

echo "#####"
####### EVALUATION: FIGURE 1 #######

echo "Compute Number of successes with each scoring function (Figure 1)"
if [ ! -d FIGURE1 ]
then
mkdir FIGURE1
fi

echo "frequency_set Score NB_success" > FIGURE1/NB_success.txt
for N in 50 100 1000 2000
do
    for SCORE in contact_average contact_sum residue_average residue_sum
    do
    result=`python $SRC_DIR/Compute_NB_success.py --score $SCORE --list listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores $WORK_DIR/Scores_Freq_top$N/  --rmsd 2.5 --N_native 0`  
    echo $N $SCORE $result 
    done
done >> FIGURE1/NB_success.txt

echo "#####"
####### EVALUATION: FIGURE 2 #######

echo "Compute Number of successes with each scoring function after combination with ZDOCK poses (Figure 2)"
if [ ! -d FIGURE2 ]
then
mkdir FIGURE2
fi

echo "frequency_set Score NB_success" > FIGURE2/NB_success.txt
for N in 50 100 1000 2000
do
    for SCORE in contact_average contact_sum residue_average residue_sum
    do
    result=`python $SRC_DIR/Compute_NB_success.py --score $SCORE --list listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores $WORK_DIR/Scores_Freq_top$N/  --rmsd 2.5`
    echo $N $SCORE $result 
    done
done >> FIGURE2/NB_success.txt


python $SRC_DIR/Compute_NB_success.py --score residue_sum --list listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores $WORK_DIR/Scores_Freq_top100/  --rmsd 2.5 --N_native 7 --verbose True > Combination_pose_stat100_N_Native7_Residue_Sum.txt

echo "1E6E" > list.temp
python $SRC_DIR/Compute_NB_success.py --score residue_sum --list list.temp  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores $WORK_DIR/Scores_Freq_top100/  --rmsd 2.5 --N_native 7 --verbose Ultra > 1E6E_pose_stat100_N_Native7_Residue_Sum.txt


echo " Compute Number of successes with each scoring function after clustering with BSAS and combination with ZDOCK clusters (Figure 3)"
if [ ! -d FIGURE3 ]
then
mkdir FIGURE3
fi

echo "#####"
####### EVALUATION: FIGURE 3 #######

echo "frequency_set Score NB_success" > FIGURE3/NB_success.txt
for N in 50 100 1000 2000
do
    for SCORE in contact_average contact_sum residue_average residue_sum
    do 
    result=`python $SRC_DIR/Combine_BSAS_clusters_Nrange.py --score $SCORE --list listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --maxD 8 --all_scores $WORK_DIR/Scores_Freq_top$N/  --rmsd 2.5`
    echo $N $SCORE $result 
    done
done >> FIGURE3/NB_success.txt


echo "#####"
####### EVALUATION: FIGURE 4 #######

# To retrieve the selected pose, run  with the option --verbose Ultra
echo "1AVX
1EAW
1XQS
1E6E" > list.txt

python $SRC_DIR/Combine_BSAS_clusters_Nrange.py --N_native 5 --verbose Ultra --score contact_sum --maxD 8 --list list.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores $WORK_DIR/Scores_Freq_top1000/  --rmsd 2.5 > poses_figure4.txt

