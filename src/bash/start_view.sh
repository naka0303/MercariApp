#!/usr/bin/env bash
#
# DATE:   2022-12-18
# UPDATE: 2023-01-08
# PURPOSE:
#   - 検索文字列入力フォームを生成し、その文字列を受け取りファイルに出力
# USAGE:
#   ./start_view.sh
# NOTES:
#   - 本shは、cronでは実行しないこと


### 変数宣言 ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../; pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs/; pwd)
readonly SRC_DIR=$(cd $APP_DIR/src; pwd)
readonly TMP_DIR=$(cd $APP_DIR/tmp; pwd)
readonly YYYYMMDD=$(date '+%Y-%m-%d')
readonly HHMMSS=$(date '+%h-%m-%s')
readonly LOG_NAME=${YYYYMMDD}_${SCRIPT_NAME}_log

### 関数宣言 ###
# ログ関数
logger() {
    msg=$1

    now_date=$(date '+%Y-%m-%d %T')
    echo $now_date $msg >> $LOG_DIR/bash/$LOG_NAME.txt
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
    logger "${YYYYMMDD}_start_view.py_log.txtを確認"
    logger "==========================="
    return 1
}

### 処理開始 ###
start $SCRIPT_NAME

### 変数確認 ###
logger "APP_DIR: $APP_DIR"
logger "SCRIPT_NAME: $SCRIPT_NAME"
logger "LOG_DIR: $LOG_DIR"
logger "SRC_DIR: $SRC_DIR"
logger "TMP_DIR: $TMP_DIR"
logger "YYYYMMDD: $YYYYMMDD"
logger "HHMMSS: $HHMMSS"
logger "LOG_NAME: $LOG_NAME"
logger "output_log_file: $LOG_DIR/bash/$LOG_NAME.txt"

### 検索文字列入力フォームを生成し、その文字列を受け取りファイルに出力 ###
#     ex) output_file_name: 2022-12-18_12-12-1671297826.txt
logger "[EXEC] start_view.py"
python3 $SRC_DIR/py/start_view.py $YYYYMMDD $HHMMSS

# tmp下にファイルが出力されたか確認
readonly txt_num=$(ls $TMP_DIR | grep -e $YYYYMMDD | grep -e $HHMMSS | wc -l)
if [ $txt_num -eq 0 ]; then
    ### 処理異常終了 ###
    abend
fi

logger "[END] start_view.py"

### 処理正常終了 ###
normal_end
