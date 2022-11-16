#!/usr/bin/env bash
#
# DATE:  2022-11-12
# PURPOSE:
#   - csvディレクトリ直下の「<yyyy-mm-dd-hh-mm-ss>_all_product.csv」と、
#     「<yyyy-mm-dd-hh-mm-ss>_first_product_description.csv」を日別ディレクトリに格納する
# NOTES:
#   - このshはcronで動かすようにすること(開発時に単発実行するのはOK)
#


### 変数セット ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../; pwd)
# readonly SCRIPT_HOMEDIR=$(cd $(dirname $0); pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs; pwd)
readonly CSV_DIR=$(cd $APP_DIR/csv; pwd)
readonly TODAY=$(date '+%Y-%m-%d')
readonly LOG_NAME=${TODAY}_${SCRIPT_NAME}_log

### 関数作成 ###
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

### 変数確認 ###
logger "APP_DIR: $APP_DIR"
logger "SCRIPT_NAME: $SCRIPT_NAME"
logger "LOG_DIR: $LOG_DIR"
logger "CSV_DIR: $CSV_DIR"
logger "TODAY: $TODAY"
logger "LOG_NAME: $LOG_NAME"

### 実処理 ###
# csvディレクトリ直下に、今日の日付ディレクトリを作成する
mkdir -p $CSV_DIR/$TODAY

# csvディレクトリ直下にある今日の日付のCSVファイルを、上記作成ディレクトリに移動する
mv $CSV_DIR/$TODAY-*.csv $CSV_DIR/$TODAY/

# 処理正常終了
normal_end
