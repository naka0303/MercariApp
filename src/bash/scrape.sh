#!/usr/bin/env bash
#
# DATE:   2022-11-23
# UPDATE: 2023-01-08
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
    abend
fi

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

### 変数セット ###
readonly newest_txt=$(ls -rt $TMP_DIR/* | tail -n 1)
readonly search_word1=$(sed -n '1p' $newest_txt)
readonly search_word2=$(sed -n '2p' $newest_txt)
readonly search_word3=$(sed -n '3p' $newest_txt)
readonly status=$(sed -n '4p' $newest_txt)
readonly sort_order=$(sed -n '5p' $newest_txt)

### 変数確認 ###
logger "search_word1: $search_word1"
logger "search_word2: $search_word2"
logger "search_word3: $search_word3"
logger "status: $status"
logger "sort_order: $sort_order"

# スクレイピング前のcsvディレクトリ下の総ファイル数取得
readonly before_csv_num=$(ls $CSV_DIR | wc -l)

# メルカリ画面のスクレイピングを行い、インデックス番号と価格と商品名と画像URLのリストをCSVに出力する
# FIXME: serch_wordは、3つ未満でも実行できるようにする
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
