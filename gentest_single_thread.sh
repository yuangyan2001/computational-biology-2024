mkdir -p test_dir_single_thread
cd ./test_dir_single_thread &&
OUTPUT_DIR="single_thread_result/"
mkdir -p $OUTPUT_DIR

for file in "../truncate_160bp/"*
do
    SCRIPT=$(basename ${file})_test_single_thread.sh
    QUERY_LEN=$(echo "$SCRIPT" | grep -oP '\d+' | head -n 1)



    rm -rf $SCRIPT
    echo "#!/bin/bash" >> $SCRIPT
    echo "#SBATCH --account=rrg-regrant" >> $SCRIPT
    echo "#SBATCH --nodes=1" >> $SCRIPT
    echo "#SBATCH --ntasks-per-node=1" >> $SCRIPT
    echo "#SBATCH --exclusive" >> $SCRIPT
    echo "#SBATCH --time=05:59:00" >> $SCRIPT
    echo "#SBATCH --mem=0" >> $SCRIPT
    
    echo "mkdir -p  \$SLURM_TMPDIR/db" >> $SCRIPT
    echo "mkdir -p \$SLURM_TMPDIR/query" >> $SCRIPT
    echo "cp /home/yuangyan/projects/def-regrant/yuangyan/cisc882/BLASTdb/* \$SLURM_TMPDIR/db" >> $SCRIPT
    echo "cp $file \$SLURM_TMPDIR/query" >> $SCRIPT
    echo "for i in 1 2 3" >> $SCRIPT
    echo "do" >> $SCRIPT
    echo "perf stat -d -d -d -o ./$OUTPUT_DIR$(basename ${file})_single_thread_res_\$i  blastn -db \$SLURM_TMPDIR/db/nt -query \$SLURM_TMPDIR/query/$(basename ${file}) -out results.out -evalue 1e-5 -num_threads 1" >> $SCRIPT

    echo "done" >> $SCRIPT

done
cd ..