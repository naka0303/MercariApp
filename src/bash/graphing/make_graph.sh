#!/usr/bin/env bash
#
# DATE:  2022-12-15
# PURPOSE:
#   - 引数で指定したcsvファイルのグラフを作成する
# NOTES:
#   - このshはcronでは動かさない想定
#


### 変数セット ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../; pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs; pwd)
readonly SRC_DIR=$(cd $APP_DIR/src; pwd)
readonly CSV_DIR=$(cd $APP_DIR/csv; pwd)
readonly YYYYMMDD=$(date '+%Y-%m-%d')
readonly HHMMSS=$(date '+%h-%m-%s')
readonly LOG_NAME=${YYYYMMDD}_${SCRIPT_NAME}_log

# ログ関数
logger() {
    msg=$1

    now_date=$(date '+%Y-%m-%d %T')
    echo $now_date $msg >> $LOG_DIR/bash/$LOG_NAME 
}

# 処理開始用関数
start() {
    script_name=$1
    logger "========== START $script_name =========="
}

# 処理正常終了用関数
normal_end() {
    logger "========== NORMAL END =========="
    return 0
}

# 処理開始
start $SCRIPT_NAME

python3 $SRC_DIR/py/make_graph.py $CSV_DIR/2022-12-17-22-08-55_all_product.csv

# 処理正常終了
normal_end
