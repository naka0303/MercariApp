from selenium.webdriver.common.by import By
import csv
import logger

SLEEP_TIME = 20

# メルカリ画面のスクレイピング実行
def scrape(driver, args):
    # 検索ワード
    search_word = '%20'.join(args)

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

    logger.info('SEARCH_WORD: ' + search_word)
    logger.info('STATUS: ' + status)
    logger.info('SORT_ORDER: ' + sort_order)

    # メルカリ公式サイトを開く
    driver.get("https://jp.mercari.com/search?keyword=" + search_word + "&" + sort_order + "&" + status)

    # 出品商品情報取得
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
