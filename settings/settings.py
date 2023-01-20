import datetime
import socket
import os


# 現在時刻
DT_NOW = datetime.datetime.now()

# 実行ホスト
HOSTNAME = socket.gethostname()

# 要素探索待機時間
SLEEP_TIME = 30

# 各ディレクトリパス
APP_DIR_PATH = os.getcwd()
CSV_DIR_PATH = APP_DIR_PATH + '/csv'
DRIVER_DIR_PATH = APP_DIR_PATH + '/driver'
GRAPH_DIR_PATH = APP_DIR_PATH + '/graph'
PY_LOGS_DIR_PATH = APP_DIR_PATH + '/logs/py'
BASH_LOGS_DIR_PATH = APP_DIR_PATH + '/logs/bash'
SRC_DIR_PATH = APP_DIR_PATH + '/src'
TMP_DIR_PATH = APP_DIR_PATH + '/tmp'

# 販売状況
# - 販売中 : status=on_sale
# - 売り切れ : status=sold_out
STATUS_ON_SALE = 'status=on_sale' 
STATUS_SOLD_OUT = 'status=sold_out'

# 並び替え
# - 新しい順 : order=desc&sort=created_time
# - おすすめ順 : sort=score&order=desc
# - 価格の安い順 : order=asc&sort=price
# - 価格の高い順 : sort=price&order=desc
# - いいね順 : order=desc&sort=num_likes
SORT_CREATED_TIME = 'sort=score&order=desc'
SORT_SCORE = 'sort=score&order=desc'
SORT_PRICE_ASC = 'order=asc&sort=price'
SORT_PRICE_DESC = 'sort=price&order=desc'
SORT_NUM_LIKES = 'order=desc&sort=num_likes'

# スクレイピングを行うページ数
LOOP_NUM = 3
