import csv
import math
import matplotlib.pyplot as plt
import os
import sys
os.chdir('../../')
sys.path.append(os.getcwd() + '/py/loggings/')
sys.path.append(os.getcwd() + '/py/dating/')
import log_outputter
import date_formatter
import time
import datetime
import socket
import traceback


try:
    # 処理時間計測開始
    START = time.perf_counter()

    # 現在時刻取得
    DT_NOW = datetime.datetime.now()

    # 実行ホスト確認
    hostname = socket.gethostname()

    # 各ディレクトリパス格納
    os.chdir('../')
    APP_DIR_PATH = os.getcwd()
    SRC_DIR_PATH = APP_DIR_PATH + '/src'
    CSV_DIR_PATH = APP_DIR_PATH + '/csv'
    LOGS_DIR_PATH = APP_DIR_PATH + '/logs'
    IMG_DIR_PATH = APP_DIR_PATH + '/img'
    GRAPH_DIR_PATH = APP_DIR_PATH + '/graph'
    OAUTH_DIR_PATH = APP_DIR_PATH + '/oauth'

    # 実行ファイル名取得
    RUN_FILENAME = os.path.basename(__file__)

    # インスタンス生成
    log_outputter = log_outputter.LogOutputter(APP_DIR_PATH, LOGS_DIR_PATH, RUN_FILENAME)
    date_formatter = date_formatter.DateFormatter()

    # 日時のフォーマットを任意の形式に変更
    yyyymmdd, yyyymmddhhmmss = date_formatter.format_date()

    # ログファイル名
    LOG_FILE = yyyymmdd + '_' + RUN_FILENAME + '_log.txt'

    # 空のログファイルをlogsディレクトリ下に生成
    log_outputter.make_logfile(LOG_FILE)

    log_outputter.info('========== START APP ==========', LOG_FILE)
    log_outputter.info('RUNTIME: ' + str(DT_NOW), LOG_FILE)
    log_outputter.info('APP_DIR_PATH: ' + APP_DIR_PATH, LOG_FILE)
    log_outputter.info('SRC_DIR_PATH: ' + SRC_DIR_PATH, LOG_FILE)
    log_outputter.info('IMG_DIR_PATH: ' + IMG_DIR_PATH, LOG_FILE)
    log_outputter.info('GRAPH_DIR_PATH: ' + GRAPH_DIR_PATH, LOG_FILE)
    log_outputter.info('CSV_DIR_PATH: ' + CSV_DIR_PATH, LOG_FILE)
    log_outputter.info('LOGS_DIR_PATH: ' + LOGS_DIR_PATH, LOG_FILE)
    log_outputter.info('OUTPUT_LOG_PATH: ' + LOGS_DIR_PATH + '/' + LOG_FILE, LOG_FILE)

    # 引数チェック
    args = sys.argv
    if (len(args) == 2):
        log_outputter.info('ARGS1: ' + args[1], LOG_FILE)
    else:
        raise Exception

    ### csvから価格帯を取得する ###
    # (1) 価格リストを昇順にする
    # (2) 昇順にした価格リストから、最低価格と最高価格を取得する
    # (3) 最低価格の最上位桁の値を右ゼロ埋めした値を、グラフの横軸の下限値として決定する
    # (4) 最高価格の最上位桁の値に1加えた値を、さらに右ゼロ埋めした値を、グラフの横軸の上限値として決定する
    # (5) 最高価格と最低価格の差を取得する
    # (6) 横軸を10個にできるよう以下のように価格の分け方を決定する
    # (7) (6)で決定された価格分割に沿って、価格リストを分割していく

    prices = []
    with open(args[1] + '.csv', 'r') as f:
        reader = csv.reader(f)
        for r in reader:
            prices.append(int(r[2]))

    ## (1)価格リストを昇順にする
    prices_sorted = sorted(prices)

    ## (2)昇順にした価格リストから、最低価格と最高価格を取得する
    price_min = prices_sorted[0]
    price_max = prices_sorted[-1]

    ## (3)最低価格の最上位桁の値をゼロ埋めした値を、グラフの横軸の下限値を決定する
    # price_min_str = str(price_min)
    # price_min_digits = len(price_min_str)
    # lower_limit = int(price_min_str[0].ljust(price_min_digits, '0'))
    
    ## (4)最高価格の最上位桁の値に1加えた値を、さらに右ゼロ埋めした値を、グラフの横軸の上限値を決定する
    # price_max_str = str(price_max)
    # price_max_digits = len(price_max_str)
    # higher_limit = int(str(int(price_max_str[0])+1).ljust(price_max_digits, '0'))

    ## (5)最高価格と最低価格の差を取得する
    price_diff = price_max - price_min

    ## (6)横軸を10個にできるよう以下のように価格の分け方を決定する
    price_range = ''
    price_range = [math.floor(i * (price_diff / 10)) for i in range(10)]
    # if price_diff < 1000:
    #     price_range = [i*100 for i in range(10)]
    # elif 1000 <= price_diff and price_diff < 10000:
    #     price_range = [i*1000 for i in range(10)]
    # else:
    #     price_range = [i*10000 for i in range(10)]

    ## (7) (6)で決定された価格分割に沿って、価格リストを分割していく
    item_num_list = []
    for i in range(len(price_range)):
        if i == 0:
            item_num = len([price for price in prices_sorted if price < price_range[i+1]])
            item_num_list.append(item_num)
        elif i == 9:
            item_num = len([price for price in prices_sorted if price_range[i] <= price])
            item_num_list.append(item_num)
        else:
            item_num = len([price for price in prices_sorted if price_range[i] <= price and price < price_range[i+1]])
            item_num_list.append(item_num)

    # グラフの横軸（価格帯）
    left = price_range
    # グラフの縦軸（件数）
    height = item_num_list

    label = [str(price) + 'yen~' for price in price_range]
    # left = [l.replace('0', '') for l in label]

    plt.figure(figsize=(13, 5))
    plt.bar(left, height, tick_label=label, edgecolor='blue', linewidth=100, align='center', width=1)
    plt.xlabel('Price Range')
    plt.ylabel('Item Num')

    arg_splited = args[1].split('/')
    jpeg_file = GRAPH_DIR_PATH + '/' + arg_splited[-1] + '.jpeg'
    plt.savefig(jpeg_file)
    # plt.show()

except Exception:
    print(traceback.format_exc())
    # log_outputter.error(traceback.format_exc(), LOG_FILE)
    # log_outputter.error('========== ERROR ==========', LOG_FILE)


