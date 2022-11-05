from json import load
import traceback
import get_info
import logger
import os
import datetime
from selenium.webdriver.chrome import service as fs
from selenium import webdriver

try:
    # srcディレクトリパス
    SRC_PATH = os.getcwd()

    # MercariAppディレクトリパス
    os.chdir('../')
    APP_PATH = os.getcwd()
    
    # csvディレクトリパス
    CSV_PATH = APP_PATH + '/csv'
    
    # logsディレクトリパス
    LOGS_PATH = APP_PATH + "/logs"

    # 現在時刻取得
    DT_NOW = str(datetime.datetime.now())

    # LOGGERクラスのインスタンス
    logger = logger.Logger(APP_PATH, LOGS_PATH, __file__)

    # 空のログファイルをlogsディレクトリ下に生成
    logger.make_logfile()

    logger.info('========== START APP ==========')
    logger.info('RUNTIME: ' + DT_NOW)
    logger.info('SRC_PATH: ' + SRC_PATH)
    logger.info('APP_PATH: ' + APP_PATH)
    logger.info('CSV_PATH: ' + CSV_PATH)
    logger.info('LOGS_PATH: ' + LOGS_PATH)

    # 出力先csv作成
    with open(CSV_PATH + '/test.csv', 'w') as f:
        f.write('')

    # chromedriverのパス格納
    DRIVER_PATH = fs.Service(executable_path=APP_PATH + '/driver/chromedriver')

    # Chromeインスタンス作成
    driver = webdriver.Chrome(service=DRIVER_PATH)

    get_info = get_info.GetInfo(driver)

    # メルカリ画面のスクレイピング実行
    get_info.scrape()

    driver.close()

    logger.info('========== NORMAL END ==========')

except Exception:
    driver.close()

    logger.error(traceback.format_exc())
    logger.error('========== ERROR ==========')


