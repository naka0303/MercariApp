from logging import Logger
from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import traceback
import os
import csv
import logger

SLEEP_TIME = 20

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

    # LOGGERクラスのインスタンス
    logger = logger.LOGGER(APP_PATH, LOGS_PATH, __file__)

    # 空のログファイルをlogsディレクトリ下に生成
    logger.make_logfile()

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

    # 検索ワード1
    search_word1 = "ワンダム"

    # 検索ワード
    search_word2 = "ヘアアイロン"

    # 販売状況
    # - 販売中 : status=on_sale
    # - 売り切れ : status=sold_out
    status = "status=sold_out"

    # 並び替え
    # - 新しい順 : order=desc&sort=created_time
    # - おすすめ順 : sort=score&order=desc
    # - 価格の安い順 : order=asc&sort=price
    # - 価格の高い順 : sort=price&order=desc
    # - いいね順 : order=desc&sort=num_likes
    sort_order = "sort=price&order=desc"

    logger.info('search_word1: ' + search_word1)
    logger.info('search_word2: ' + search_word2)
    logger.info('status: ' + status)
    logger.info('sort_order: ' + sort_order)

    # メルカリ公式サイトを開く
    driver.get("https://jp.mercari.com/search?keyword=" + search_word1 + "%20" + search_word2 + "%20" + "&" + sort_order + "&" + status)

    ### 出品商品情報取得 ###
    driver.implicitly_wait(SLEEP_TIME)
    products = driver.find_element(By.XPATH, '//*[@id="item-grid"]/ul')

    driver.implicitly_wait(SLEEP_TIME)
    products_div = products.find_elements(By.TAG_NAME, 'div')

    # 商品ごとに商品名と価格を取得する
    name_list = []
    price_list = []
    for product in products_div:
        product_detail = product.find_element(By.TAG_NAME, 'mer-item-thumbnail')
        name = product_detail.get_attribute('alt')
        name_list.append(name)
        price = product_detail.get_attribute('price')
        price_list.append(price)

    # 商品名と価格を商品ごとに結合
    name_price = list(zip(name_list, price_list))

    # csvモジュールを使って複数行の内容をcsvに書き込み
    with open('./csv/test.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(name_price)

    driver.close()

except Exception:
    print(traceback.format_exc())
    driver.close()