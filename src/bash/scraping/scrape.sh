#!/usr/bin/env bash
#
# DATE:   2022-11-23
# UPDATE: 2022-11-26
# PURPOSE:
#   - 検索文字列入力フォームを生成し、その文字列を受け取る
#   - メルカリ画面のスクレイピングをし、取得した商品情報をスプレッドシートに出力する
# USAGE:
#   ./run.sh

### 変数セット ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../../; pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs; pwd)
readonly SRC_DIR=$(cd $APP_DIR/src; pwd)
readonly TMP_DIR=$(cd $APP_DIR/tmp; pwd)
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

abend() {
    logger "========== ABEND =========="
    return 1
}

# 処理開始
start $SCRIPT_NAME

# 変数確認
logger "APP_DIR: $APP_DIR"
logger "SCRIPT_NAME: $SCRIPT_NAME"
logger "LOG_DIR: $LOG_DIR"
logger "SRC_DIR: $SRC_DIR"
logger "TMP_DIR: $TMP_DIR"
logger "YYYYMMDD: $YYYYMMDD"
logger "HHMMSS: $HHMMSS"
logger "LOG_NAME: $LOG_NAME"
logger "output_log_file: $LOG_DIR/bash/$LOG_NAME"

# 検索文字列入力フォームで入力された文字列をテキスト出力
logger "run start_view.py"
python3 $SRC_DIR/py/displaying/start_view.py $YYYYMMDD $HHMMSS

readonly search_word1=$(sed -n '1p' $TMP_DIR/${YYYYMMDD}_${HHMMSS}.txt)
readonly search_word2=$(sed -n '2p' $TMP_DIR/${YYYYMMDD}_${HHMMSS}.txt)
readonly search_word3=$(sed -n '3p' $TMP_DIR/${YYYYMMDD}_${HHMMSS}.txt)
readonly status=$(sed -n '4p' $TMP_DIR/${YYYYMMDD}_${HHMMSS}.txt)
readonly sort_order=$(sed -n '5p' $TMP_DIR/${YYYYMMDD}_${HHMMSS}.txt)

# メルカリ画面のスクレイピングを行い、商品情報をスプレッドシートに出力する
logger 'run main.py'
python3 $SRC_DIR/py/scraping/scrape.py $search_word1 $search_word2 $search_word3 $status $sort_order

# tmpディレクトリのファイルを全削除
# rm -f $TMP_DIR/*

# 処理正常終了
normal_end
