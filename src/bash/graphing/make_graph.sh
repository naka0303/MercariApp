#!/usr/bin/env bash
#
# DATE:   2022-12-15
# UPDATE: 2022-12-19
# PURPOSE:
#   - 引数で指定したcsvファイルのグラフを作成する
# USAGE:
#   - ./make_graph.sh <csv_file>
# NOTES:
#   - このshはcronでは動かさない想定


### 変数宣言 ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../../; pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs; pwd)
readonly SRC_DIR=$(cd $APP_DIR/src; pwd)
readonly CSV_DIR=$(cd $APP_DIR/csv; pwd)
readonly GRAPH_DIR=$(cd $APP_DIR/graph; pwd)
readonly YYYYMMDD=$(date '+%Y-%m-%d')
readonly CSV_FILE=$1
readonly LOG_NAME=${YYYYMMDD}_${SCRIPT_NAME}_log

### 関数宣言 ###
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

# 処理異常終了用完了
abend() {
    logger "========== ABEND =========="
    logger "${YYYYMMDD}_make_graph.py_log.txtを確認"
    logger "==========================="
    return 1
}

### 処理開始 ###
start $SCRIPT_NAME

### 引数確認 ###
if [ $# = 0 ]; then
    logger "========== ABEND =========="
    logger "引数エラー"
    logger "==========================="
    return 1
fi

### 変数確認 ###
logger "APP_DIR: $APP_DIR"
logger "LOG_DIR: $LOG_DIR"
logger "SRC_DIR: $SRC_DIR"
logger "GRAPH_DIR: $GRAPH_DIR"
logger "LOG_NAME: $LOG_NAME"
logger "CSV_FILE: $CSV_FILE"
logger "output_log_file: $LOG_DIR/bash/$LOG_NAME"

### 引数で指定したcsvファイルのグラフを作成する ###
python3 $SRC_DIR/py/make_graph.py $CSV_DIR/$CSV_FILE

# graph下にグラフ画像が保存されたか確認
readonly jpeg_num=$(ls $GRAPH_DIR/$CSV_FILE.jpeg | wc -l)
if [ $jpeg_num -eq 0 ]; then
    ### 処理異常終了 ###
    abend
else
    ### 処理正常終了 ###
    normal_end
fi
