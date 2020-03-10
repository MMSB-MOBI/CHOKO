echo "Compute Number of successes with each scoring function after BSAS clustering AND combination with ZDOCK scores (Figure 3)"

echo "frequency_set Score N_ZDOCK NB_success" > NB_success_cluster_combination.txt
for N in 50 100 1000 2000
do
    for SCORE in contact_average contact_sum residue_average residue_sum
    do
    python $SRC_DIR/Combine_BSAS_clusters_Nrange.py --score $SCORE --list $SRC_DIR/listBM.txt  --zdock_results $ZDOCK_DIR/results/ --max_pose 2000 --maxD 8 --all_scores Scores_Freq_top$N/  --rmsd 2.5 > result.temp
    awk -v header="$N $SCORE" '{print header" "$0}' result.temp 
    done
done >> NB_success_cluster_combination.txt


