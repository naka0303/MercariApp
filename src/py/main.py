import traceback
import get_info
import date_formatter
import log_outputter
from conditioning import csv_filer, spreadsheeter
import os
import time
import datetime
from selenium.webdriver.chrome import service as fs
from selenium import webdriver
import sys

try:
    # 処理時間計測開始
    START = time.perf_counter()

    # 各ディレクトリパス格納
    SRC_PATH = os.getcwd()
    os.chdir('../../')
    APP_PATH = os.getcwd()
    CSV_PATH = APP_PATH + '/csv'
    LOGS_PATH = APP_PATH + '/logs'
    IMG_PATH = APP_PATH + '/img'
    OAUTH_PATH = APP_PATH + '/oauth'

    # 現在時刻取得
    DT_NOW = datetime.datetime.now()

    # chromedriverのパス格納
    DRIVER_PATH = fs.Service(executable_path=APP_PATH + '/driver/chromedriver')

    # 実行ファイル名取得
    run_filename = os.path.basename(__file__)

    # インスタンス生成
    log_outputter = log_outputter.LogOutputter(APP_PATH, LOGS_PATH, run_filename)
    driver = webdriver.Chrome(service=DRIVER_PATH)
    get_info = get_info.GetInfo(APP_PATH, LOGS_PATH, IMG_PATH)
    csv_filer = csv_filer.CsvFiler()
    spreadsheeter = spreadsheeter.SpreadSheeter()
    
    date_formatter = date_formatter.DateFormatter()

    # 日時のフォーマットを任意の形式に変更
    yyyymmdd, yyyymmddhhmmss = date_formatter.format_date()

    # ログファイル名
    LOG_FILE = yyyymmdd + '_log.txt'

    # 商品情報出力用csvファイル名
    ALL_PRODUCT_CSV_FILE = yyyymmddhhmmss + '_all_product.csv'

    # 空のログファイルをlogsディレクトリ下に生成
    log_outputter.make_logfile(LOG_FILE)

    log_outputter.info('========== START APP ==========', LOG_FILE)
    log_outputter.info('RUNTIME: ' + str(DT_NOW), LOG_FILE)
    log_outputter.info('SRC_PATH: ' + SRC_PATH, LOG_FILE)
    log_outputter.info('APP_PATH: ' + APP_PATH, LOG_FILE)
    log_outputter.info('IMG_PATH: ' + IMG_PATH, LOG_FILE)
    log_outputter.info('ALL_PRODUCT_CSV_FILE: ' + CSV_PATH, LOG_FILE)
    log_outputter.info('PRODUCT_DESCRIPTION_CSV_FILE: ' + CSV_PATH, LOG_FILE)
    log_outputter.info('LOGS_PATH: ' + LOGS_PATH, LOG_FILE)

    # 引数取得
    args = sys.argv
    if (len(args) == 1):
        raise Exception
    
    for i in range(len(args[1:])):
        log_outputter.info('ARGS' + str(i + 1) + ': ' + args[i + 1], LOG_FILE)

    # 出力先csv作成
    with open(CSV_PATH + '/' + ALL_PRODUCT_CSV_FILE, 'w') as f:
        f.write('')

    # メルカリ画面のスクレイピング実行
    all_idx_name_price_img = get_info.scrape(driver, args[1:], LOG_FILE)

    # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
    all_idx_name_price_img_removed = csv_filer.remove_unneeded(args[1:], all_idx_name_price_img)

    log_outputter.info('PRODUCT_COUNT: ' + str(len(all_idx_name_price_img_removed)), LOG_FILE)

    # 全商品情報をcsvに出力
    csv_filer.write_data(CSV_PATH, ALL_PRODUCT_CSV_FILE, all_idx_name_price_img_removed, 'w')

    # スプレッドシート書き込み(テスト)
    spreadsheeter.make_sheet(OAUTH_PATH, all_idx_name_price_img_removed)

    driver.close()

    # 処理時間計測終了
    END = time.perf_counter()

    # 経過時間（秒）
    PROCESS_TIME = END - START

    log_outputter.info('PROCESS_TIME: ' + str(PROCESS_TIME), LOG_FILE)

    log_outputter.info('========== NORMAL END ==========', LOG_FILE)

except Exception:
    driver.close()

    log_outputter.error(traceback.format_exc(), LOG_FILE)
    log_outputter.error('========== ERROR ==========', LOG_FILE)
