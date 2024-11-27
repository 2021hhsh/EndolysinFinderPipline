#!/bin/bash

# 默认值
INPUT_DIR="input"
#OUTPUT_DIR="vibrant-output"
FNAS_DIR="fnas"
CHECKV_OUTPUT_DIR="checkv_output"
GBK_FAA_OUT_DIR="gbk-faa-out"
CHECKED_SEQS_DIR="checked_seqs"
HMMER_INPUT_DIR="hmmer-input-uniq"
HMM_RUN_DIR="hmm_run"
RESULT_DIR="$HMM_RUN_DIR/result"
VIBRANT_ENV="new_vibrant"
CHECKV_ENV="checkv"
CHECKV_DB="../checkv_db/checkv-db-v1.5"
HMMER_DB="~/miniconda3/envs/new_vibrant/share/vibrant-1.2.1/db/databases/Pfam-A_v32.HMM"
HMMSEARCH_MODEL_DIR="../hmmer_mod"
THREADS=10
PROCESSES=1

# 帮助文档
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h                 Show help documentation"
    echo "  -i <input_dir>     Specify the input directory (default: input)"
    #echo "  -o <output_dir>    Specify the output directory for Vibrant (default: vibrant-output)"
    echo "  -v <vibrant_env>   Specify the Vibrant conda environment name (default: new_vibrant)"
    echo "  -c <checkv_env>    Specify the CheckV conda environment name (default: checkv)"
    echo "  -d <checkv_db>     Specify the CheckV database path (default: ../checkv_db/checkv-db-v1.5)"
    echo "  -b <hmmscan_db>    Specify the hmmscan database path (default: Pfam-A_v32.HMM)"
    echo "  -s <model_dir>     Specify the hmmsearch model input directory (default: ../hmmer_mod)"
    echo "  -t <threads>       Specify the number of threads per process (default: 10)"
    echo "  -n <processes>     Specify the number of parallel processes (default: 3)"
    exit 0
}

# 解析命令行参数
while getopts ":hi:o:v:c:d:b:s:t:n:" opt; do
    case $opt in
        h)
            usage
            ;;
        i)
            INPUT_DIR=$OPTARG
            ;;
        #o)
        #    OUTPUT_DIR=$OPTARG
        #    ;;
        v)
            VIBRANT_ENV=$OPTARG
            ;;
        c)
            CHECKV_ENV=$OPTARG
            ;;
        d)
            CHECKV_DB=$OPTARG
            ;;
        b)
            HMMER_DB=$OPTARG
            ;;
        s)
            HMMSEARCH_MODEL_DIR=$OPTARG
            ;;
        t)
            THREADS=$OPTARG
            ;;
        n)
            PROCESSES=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            usage
            ;;
    esac
done

# 函数：检查上一步命令是否成功
check_command() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed. Exiting."
        exit 1
    fi
}

# 函数：打印日志
log() {
    echo "========== $1 =========="
}

# 激活 Vibrant 环境并运行
log "Running Vibrant in environment: $VIBRANT_ENV"
conda run -n $VIBRANT_ENV python scripts/multi-vibrant.py -i $INPUT_DIR -n $PROCESSES -t $THREADS
check_command "Running Vibrant"

# 运行 get_fna.py 提取 .fna 文件
log "Running get_fna.py"
conda run -n $VIBRANT_ENV python scripts/get_fna.py
check_command "Running get_fna.py"

# 激活 CheckV 环境并运行
log "Running CheckV in environment: $CHECKV_ENV"
conda run -n $CHECKV_ENV python scripts/run_checkV.py -i $FNAS_DIR -o $CHECKV_OUTPUT_DIR -d $CHECKV_DB -t $THREADS -n $PROCESSES
check_command "Running CheckV"

# 提取 Vibrant 的蛋白序列文件
log "Extracting protein sequences with get_gbk-trans-faa.py"
conda run -n $VIBRANT_ENV python scripts/get_gbk-trans-faa.py
check_command "Extracting protein sequences"

# 筛选前噬菌体 faa 文件
log "Filtering sequences with checkv-out-faa-copy.py"
conda run -n $CHECKV_ENV python scripts/checkv-out-faa-copy.py $CHECKV_OUTPUT_DIR $GBK_FAA_OUT_DIR $CHECKED_SEQS_DIR
check_command "Filtering sequences"

# 创建合并目录并去重
log "Creating HMMER input directory and deduplicating sequences"
mkdir -p $HMMER_INPUT_DIR

if ls $CHECKED_SEQS_DIR/*.faa 1> /dev/null 2>&1; then
    # 合并 .faa 文件
    cat $CHECKED_SEQS_DIR/*.faa > ${HMMER_INPUT_DIR}/hmmer_in_seq.faa
else
    # 提示错误并终止程序
    echo "Error: No suitable .faa files found in $CHECKED_SEQS_DIR. Exiting."
    exit 1
fi
# 去重
conda run -n $VIBRANT_ENV python scripts/unique_seq.py ${HMMER_INPUT_DIR}/hmmer_in_seq.faa  

check_command "Deduplicating sequences"

# 创建 HMMER 运行目录
log "Creating HMMER run directory"
mkdir -p $HMM_RUN_DIR/out
check_command "Creating HMMER run directory"

# 运行 HMMER
log "Running HMMER"
cd $HMM_RUN_DIR
conda run -n $VIBRANT_ENV python ../scripts/hmmer_search.py -t $((THREADS*PROCESSES)) -d $HMMSEARCH_MODEL_DIR 
check_command "Running HMMER"

# 提取 HMMER 搜索结果
log "Extracting HMMER results"
conda run -n $VIBRANT_ENV python ../scripts/hmmer-result-extract_new.py
check_command "Extracting HMMER results"

# 按权重排序
log "Sorting HMMER results"
conda run -n $VIBRANT_ENV python ../scripts/hmmer-result-sort.py > sorted.txt
check_command "Sorting HMMER results"

# 提取序列
log "Extracting sequences"
conda run -n $VIBRANT_ENV python ../scripts/extract_seq.py
check_command "Extracting sequences"

# 注释并生成结果表
log "Annotating sequences and generating result tables"
#mkdir -p $RESULT_DIR
#rm -fr $RESULT_DIR/*
conda run -n $VIBRANT_ENV python ../scripts/hmmer_scan.py  -t $((THREADS*PROCESSES)) -d $HMMER_DB
check_command "Annotating sequences"

conda run -n $VIBRANT_ENV python ../scripts/get_result.py
check_command "Generating result table"

conda run -n $VIBRANT_ENV python ../scripts/get_aa_seq.py
check_command "Generating annotated sequences"

conda run -n $VIBRANT_ENV python ../scripts/recall.py
check_command "Recalling sequences"

conda run -n $VIBRANT_ENV python ../scripts/july_Y.py > ../final.txt
check_command "Finalizing results"
cd ..

log "Pipeline completed successfully!"

