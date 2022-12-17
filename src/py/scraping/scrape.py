import traceback
import socket
import get_info
import date_formatter
from .. logging import log_outputter
from .. conditioning import csv_filer, spreadsheeter
import os
import time
import datetime
from selenium.webdriver.chrome import service as fs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

try:
    # 処理時間計測開始
    START = time.perf_counter()

    # 現在時刻取得
    DT_NOW = datetime.datetime.now()

    # 実行ホスト確認
    hostname = socket.gethostname()

    # 各ディレクトリパス格納
    os.chdir('../../../')
    APP_DIR_PATH = os.getcwd()
    SRC_DIR_PATH = APP_DIR_PATH + '/src'
    CSV_DIR_PATH = APP_DIR_PATH + '/csv'
    LOGS_DIR_PATH = APP_DIR_PATH + '/logs'
    IMG_DIR_PATH = APP_DIR_PATH + '/img'
    OAUTH_DIR_PATH = APP_DIR_PATH + '/oauth'

    driver_dir_path = ''
    options = Options()
    options.headless = True

    if ('local' in hostname):
        # chromedriverパス格納
        driver_dir_path = APP_DIR_PATH + '/driver'
        DRIVER_PATH = fs.Service(executable_path=driver_dir_path + '/chromedrive')
        driver = webdriver.Chrome(service=DRIVER_PATH, options=options)
    else:
        import chromedriver_binary
        driver = webdriver.Chrome(options=options)

    # 実行ファイル名取得
    RUN_FILENAME = os.path.basename(__file__)

    # インスタンス生成
    log_outputter = log_outputter.LogOutputter(APP_DIR_PATH, LOGS_DIR_PATH, RUN_FILENAME)
    get_info = get_info.GetInfo(APP_DIR_PATH, LOGS_DIR_PATH, IMG_DIR_PATH)
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
    log_outputter.info('driver_dir_path: ' + driver_dir_path, LOG_FILE)
    log_outputter.info('APP_DIR_PATH: ' + APP_DIR_PATH, LOG_FILE)
    log_outputter.info('SRC_DIR_PATH: ' + SRC_DIR_PATH, LOG_FILE)
    log_outputter.info('IMG_DIR_PATH: ' + IMG_DIR_PATH, LOG_FILE)
    log_outputter.info('CSV_DIR_PATH: ' + CSV_DIR_PATH, LOG_FILE)
    log_outputter.info('LOGS_DIR_PATH: ' + LOGS_DIR_PATH, LOG_FILE)
    log_outputter.info('OUTPUT_LOG_PATH: ' + LOGS_DIR_PATH + '/' + LOG_FILE, LOG_FILE)

    # 出力先csv作成
    with open(CSV_DIR_PATH + '/' + ALL_PRODUCT_CSV_FILE, 'w') as f:
        f.write('')
    log_outputter.info('OUTPUT_CSV_PATH: ' + CSV_DIR_PATH + '/' + ALL_PRODUCT_CSV_FILE, LOG_FILE)

    # 引数チェック
    args = sys.argv
    if (len(args) == 1):
        raise Exception
    for i in range(len(args[1:])):
        log_outputter.info('ARGS' + str(i + 1) + ': ' + args[i + 1], LOG_FILE)

    # メルカリ画面のスクレイピング実行
    all_idx_name_price_img = get_info.scrape(driver, args[1:], LOG_FILE)

    # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
    all_idx_name_price_img_removed = csv_filer.remove_unneeded(args[1:], all_idx_name_price_img)
    log_outputter.info('PRODUCT_COUNT: ' + str(len(all_idx_name_price_img_removed)), LOG_FILE)

    # 全商品情報をcsvに出力
    csv_filer.write_data(CSV_DIR_PATH, ALL_PRODUCT_CSV_FILE, all_idx_name_price_img_removed, 'w')

    # スプレッドシート書き込み
    # spreadsheeter.make_sheet(OAUTH_DIR_PATH, yyyymmddhhmmss, all_idx_name_price_img_removed)

    driver.close()

    # 処理時間計測終了
    END = time.perf_counter()

    # 経過時間(秒)
    PROCESS_TIME = END - START

    log_outputter.info('PROCESS_TIME: ' + str(PROCESS_TIME), LOG_FILE)
    log_outputter.info('========== NORMAL END ==========', LOG_FILE)

except Exception:
    driver.close()

    log_outputter.error(traceback.format_exc(), LOG_FILE)
    log_outputter.error('========== ERROR ==========', LOG_FILE)
