#!/usr/bin/env bash
#
# DATE:  2022-11-23
# PURPOSE:
#   - 検索文字
# NOTES:
#


### 変数セット ###
readonly APP_DIR=$(cd $(dirname $0); cd ../../; pwd)
# readonly SCRIPT_HOMEDIR=$(cd $(dirname $0); pwd)
readonly SCRIPT_NAME=$(basename $0)
readonly LOG_DIR=$(cd $APP_DIR/logs; pwd)
readonly CSV_DIR=$(cd $APP_DIR/csv; pwd)
readonly SRC_DIR=$(cd $APP_DIR/src; pwd)
readonly TMP_DIR=$(cd $APP_DIR/tmp; pwd)
readonly TODAY=$(date '+%Y-%m-%d')
readonly LOG_NAME=${TODAY}_${SCRIPT_NAME}_log

# 検索文字列入力フォームで入力された文字列をテキスト出力
python3 $SRC_DIR/py/displaying/start_view.py

readonly arg1=$(sed -n '1p' $TMP_DIR/test.txt)
readonly arg2=$(sed -n '2p' $TMP_DIR/test.txt)
readonly arg3=$(sed -n '3p' $TMP_DIR/test.txt)

echo $arg1 $arg2 $arg3



