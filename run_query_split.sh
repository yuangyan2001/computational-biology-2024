cd ./test_dir_query_split
for file in "."/*
do
    if [ -f "$file" ]; then  
        QUERY_LEN=$(echo $(basename ${file}) | grep -oP '\d+' | head -n 1)
        if [[ $QUERY_LEN -ge 16384 ]]; then
            sbatch $file
            # echo $(basename ${file})
        fi
    fi

done
cd ..