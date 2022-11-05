from selenium.webdriver.common.by import By
import csv
import logger

SLEEP_TIME = 20

# メルカリ画面のスクレイピング実行
def scrape(driver):
    # 検索ワード1
    search_word1 = "僕なんか"

    # 検索ワード2
    search_word2 = "初回限定盤"

    # 検索ワード3
    search_word3 = "4枚セット"

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
    sort_order = "order=asc&sort=price"

    logger.info('search_word1: ' + search_word1)
    logger.info('search_word2: ' + search_word2)
    logger.info('search_word3: ' + search_word3)
    logger.info('status: ' + status)
    logger.info('sort_order: ' + sort_order)

    # メルカリ公式サイトを開く
    driver.get("https://jp.mercari.com/search?keyword=" + search_word1 + "%20" + search_word2 + "%20" + search_word3 + "&" + sort_order + "&" + status)

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

    return name_price
