for N in 50 100 1000 2000 
do
mkdir Freq_top$N
cd Freq_top$N  
python $SRC_DIR/Compute_frequencies.py --list $SRC_DIR/listBM.txt --zdock_results $ZDOCK_DIR/results/ --input_pdb $ZDOCK_DIR/input_pdbs/ --N $N
cd ..
done 

