from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import traceback
import os
import time

SLEEP_TIME = 20

try:
    # MercariAppのディレクトリパス
    app_path = os.getcwd()

    # chromedriverのパス格納
    driver_path = fs.Service(executable_path=app_path + '/chromedriver')

    # Chromeインスタンス作成
    driver = webdriver.Chrome(service=driver_path)

    # 検索ワード1
    search_word1 = "ワンダム"

    # 検索ワード
    search_word2 = "ヘアアイロン"

    # 販売状況
    # - 販売中 : status=on_sale
    status = "status=on_sale"

    # 並び替え
    # - 新しい順 : order=desc&sort=created_time
    # - おすすめ順 : sort=score&order=desc
    # - 価格の安い順 : order=asc&sort=price
    # - 価格の高い順 : sort=price&order=desc
    # - いいね順 : order=desc&sort=num_likes
    sort_order = "sort=price&order=desc"

    # メルカリ公式サイトを開く
    driver.get("https://jp.mercari.com/search?keyword=" + search_word1 + "%20" + search_word2 + "%20" + "&" + sort_order + "&" + status)

    # 出品商品情報取得
    driver.implicitly_wait(SLEEP_TIME)
    products = driver.find_element(By.XPATH, '//*[@id="item-grid"]/ul')

    print(products)
    print("a")

    driver.implicitly_wait(SLEEP_TIME)
    products_div = products.find_element(By.TAG_NAME, 'div')

    print("b")

    product_cells = products_div.find_elements(By.TAG_NAME, 'div')

    print("c")
    print(type(product_cells))

    driver.close()

except Exception:
    print(traceback.format_exc())
    driver.close()