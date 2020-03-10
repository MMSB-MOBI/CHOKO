for N in 50 100 1000 2000 
do

mkdir Scores_Freq_top$N
cd Scores_Freq_top$N

    for protein in `cat $SRC_DIR/listBM.txt `
    do
    echo $protein > list.temp
        if [ ! -e $protein.tsv ]
        then
        echo Scores_Freq_top$N $protein 
        python $SRC_DIR/Compute_scores_from_pkl.py --list list.temp --zdock_results $ZDOCK_DIR/results/ --input_pdb $ZDOCK_DIR/input_pdbs/ --N 2000 --freq_dir ..//Freq_top$N
        fi
    done
cd ..
done



