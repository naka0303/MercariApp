#!/usr/bin/env bash
#
# DATE:   2022-11-23
# UPDATE: 2023-01-14
# PURPOSE:
#   - 検索文字列入力フォームを生成し、その文字列を受け取る
#   - メルカリ画面のスクレイピングをし、取得した商品情報をスプレッドシートに出力する
# USAGE:
#   ./scrape.sh

### 変数セット ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../; pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs; pwd)
readonly CSV_DIR=$(cd $APP_DIR/csv; pwd)
readonly SRC_DIR=$(cd $APP_DIR/src; pwd)
readonly TMP_DIR=$(cd $APP_DIR/tmp; pwd)
readonly YYYYMMDD=$(date '+%Y-%m-%d')
readonly HHMMSS=$(date '+%h-%m-%s')
readonly LOG_NAME=${YYYYMMDD}_${SCRIPT_NAME}_log
readonly newest_txt=$(ls -rt $TMP_DIR/* | tail -n 1)

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
    exit 0
}

# 処理異常終了用完了
abend() {
    logger "========== ABEND =========="
    logger "${YYYYMMDD}_scrape.py_log.txtを確認"
    logger "==========================="
    exit 1
}

### 処理開始 ###
start $SCRIPT_NAME

### 変数確認 ###
logger "APP_DIR: $APP_DIR"
logger "SCRIPT_NAME: $SCRIPT_NAME"
logger "LOG_DIR: $LOG_DIR"
logger "CSV_DIR: $CSV_DIR"
logger "SRC_DIR: $SRC_DIR"
logger "TMP_DIR: $TMP_DIR"
logger "YYYYMMDD: $YYYYMMDD"
logger "HHMMSS: $HHMMSS"
logger "LOG_NAME: $LOG_NAME"
logger "output_log_file: $LOG_DIR/bash/$LOG_NAME.txt"
logger "newest_txt: $newest_txt"

### 検索文字列入力内容取得 ###


### 変数セット ###
readonly search_word1=$(cat $newest_txt | cut -d " " -f 1 | tail -n 1)
readonly search_word2=$(cat $newest_txt | cut -d " " -f 2 | tail -n 1)
readonly search_word3=$(cat $newest_txt | cut -d " " -f 3 | tail -n 1)
readonly status=$(cat $newest_txt | cut -d " " -f 4 | tail -n 1)
readonly sort_order=$(cat $newest_txt | cut -d " " -f 5 | tail -n 1)

### 変数確認 ###
logger "search_word1: $search_word1"
logger "search_word2: $search_word2"
logger "search_word3: $search_word3"
logger "status: $status"
logger "sort_order: $sort_order"

# スクレイピング前のcsvディレクトリ下の総ファイル数取得
readonly before_csv_num=$(ls $CSV_DIR | wc -l)

# メルカリ画面のスクレイピングを行い、インデックス番号と価格と商品名と画像URLのリストをCSVに出力する
# FIXME: search_wordは、3つ未満でも実行できるようにする
logger "[EXEC] scrape.py"
python3 $SRC_DIR/py/scrape.py $search_word1 $search_word2 $search_word3 $status $sort_order

# スクレイピング後のcsvディレクトリ下の総ファイル数取得
readonly after_csv_num=$(ls $CSV_DIR | wc -l)

diff_csv_num=$(expr $after_csv_num - $before_csv_num)

if [ $diff_csv_num -ne 1 ]; then
    ### 処理異常終了 ###
    abend
fi

logger "[END] scrape.py"

# tmpディレクトリのファイルを全削除
rm -f $TMP_DIR/*

# 処理正常終了
normal_end
