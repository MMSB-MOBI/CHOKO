# File reformatting
tar xzvf decoys_bm4_zd3.0.2_6deg_fixed.tar.gz 
cd decoys_bm4_zd3.0.2_6deg_fixed/input_pdbs/
        # reformat to have a parsable PDB format
        for file in `ls *.pdb.ms `; do cut -c1-55 $file > ${file%%.ms}; done

