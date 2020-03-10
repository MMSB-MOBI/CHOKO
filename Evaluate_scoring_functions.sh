echo "Compute Number of successes with each scoring function (Figure 1)"

echo "frequency_set Score NB_success" > NB_success_separate_scoring_functions.txt
for N in 50 100 1000 2000
do
    for SCORE in contact_average contact_sum residue_average residue_sum
    do
    result=`python $SRC_DIR/Compute_NB_success.py --score $SCORE --list $SRC_DIR/listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --all_scores Scores_Freq_top$N/  --rmsd 2.5 --N_native 0`  
    echo $N $SCORE $result 
    done
done >> NB_success_separate_scoring_functions.txt

