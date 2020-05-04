mkdir SCORES
cd SCORES

for N1 in 50 100 1000 2000 
do
    mkdir Freq_top$N1
    cd Freq_top$N1
    echo Freq_top$N1
    python $SRC_DIR/Compute_scores.py --list $SRC_DIR/listBM.txt --zdock_results $ZDOCK_DIR/results/ --input_pdb $ZDOCK_DIR/input_pdbs/  --N1 $N1 --N2 2000
    cd ..
done
cd ..



