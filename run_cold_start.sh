cd ./test_cold_start
for file in "."/*
do
    if [ -f "$file" ]; then  
        QUERY_LEN=$(echo $(basename ${file}) | grep -oP '\d+' | head -n 1)
        if [ $QUERY_LEN -le 4096 ]; then
            sbatch $file
            # echo $(basename ${file})
        fi
    fi

done
# cd ..