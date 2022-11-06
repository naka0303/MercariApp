import traceback
import get_info
import csv_conditioning
import logger
import os
import datetime
from selenium.webdriver.chrome import service as fs
from selenium import webdriver
import sys

try:
    # 各ディレクトリパス格納
    SRC_PATH = os.getcwd()

    os.chdir('../')
    APP_PATH = os.getcwd()
    CSV_PATH = APP_PATH + '/csv'
    LOGS_PATH = APP_PATH + "/logs"

    # 現在時刻取得
    DT_NOW = str(datetime.datetime.now())

    # chromedriverのパス格納
    DRIVER_PATH = fs.Service(executable_path=APP_PATH + '/driver/chromedriver')

    # インスタンス生成
    logger = logger.Logger(APP_PATH, LOGS_PATH, __file__)
    driver = webdriver.Chrome(service=DRIVER_PATH)
    csv_conditioning = csv_conditioning.CsvConditioning()

    # 空のログファイルをlogsディレクトリ下に生成
    logger.make_logfile()

    logger.info('========== START APP ==========')
    logger.info('RUNTIME: ' + DT_NOW)
    logger.info('SRC_PATH: ' + SRC_PATH)
    logger.info('APP_PATH: ' + APP_PATH)
    logger.info('CSV_PATH: ' + CSV_PATH)
    logger.info('LOGS_PATH: ' + LOGS_PATH)

    # 引数取得
    args = sys.argv
    if (len(args) == 1):
        raise Exception
    
    for i in range(len(args[1:])):
        logger.info('ARGS' + str(i + 1) + ': ' + args[i + 1])

    # 出力先csv作成
    with open(CSV_PATH + '/test.csv', 'w') as f:
        f.write('')

    # メルカリ画面のスクレイピング実行
    all_name_price = get_info.scrape(driver, args[1:])

    # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
    all_name_price_removed = csv_conditioning.remove_unneeded(args[1:], all_name_price)

    driver.close()

    logger.info('========== NORMAL END ==========')

except Exception:
    driver.close()

    logger.error(traceback.format_exc())
    logger.error('========== ERROR ==========')
