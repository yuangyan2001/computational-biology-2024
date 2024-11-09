#!/bin/bash
#SBATCH --account=rrg-regrant
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive
#SBATCH --time=05:59:00
#SBATCH --mem=0
mkdir -p  $SLURM_TMPDIR/db
mkdir -p $SLURM_TMPDIR/query
cp /home/yuangyan/projects/def-regrant/yuangyan/cisc882/BLASTdb/* $SLURM_TMPDIR/db
cp ../truncate_160bp/query_65536_use_truncate_160 $SLURM_TMPDIR/query
for i in {1..6}
do
perf stat -d -d -d -o ./query_split_result/query_65536_use_truncate_160_database_query_res_$i  blastn -db $SLURM_TMPDIR/db/nt -query $SLURM_TMPDIR/query/query_65536_use_truncate_160 -out results.out -evalue 1e-5 -num_threads 64 -mt_mode 1
done
