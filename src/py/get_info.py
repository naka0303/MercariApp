import os
import log_outputter
from selenium.webdriver.common.by import By

class GetInfo:

    SLEEP_TIME = 20
    run_filename = os.path.basename(__file__)

    # コンストラクタ
    def __init__(self, app_path, logs_path, img_path):
        self.app_path = app_path
        self.logs_path = logs_path
        self.log_outputter = log_outputter.LogOutputter(self.app_path, self.logs_path, self.run_filename)
        self.img_path = img_path

    # メルカリ画面のスクレイピング実行
    def scrape(self, driver, args, log_file):
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
        sort_order = "order=desc&sort=num_likes"

        self.log_outputter.info('SEARCH_WORD: ' + search_word, log_file)
        self.log_outputter.info('STATUS: ' + status, log_file)
        self.log_outputter.info('SORT_ORDER: ' + sort_order, log_file)

        # メルカリ公式サイトを開く
        driver.get("https://jp.mercari.com/search?keyword=" + search_word + "&" + sort_order + "&" + status)

        # 出品商品情報取得
        driver.implicitly_wait(self.SLEEP_TIME)
        products = driver.find_element(By.XPATH, '//*[@id="item-grid"]/ul')

        driver.implicitly_wait(self.SLEEP_TIME)
        products_div = products.find_elements(By.TAG_NAME, 'div')

        # 商品ごとに商品名と価格を取得する
        name_list = []
        price_list = []
        idx_list = []
        img_list = []
        idx = 1
        for product in products_div:
            product_detail = product.find_element(By.TAG_NAME, 'mer-item-thumbnail')

            idx_list.append(idx)
            name = product_detail.get_attribute('alt')
            name_list.append(name)
            price = product_detail.get_attribute('price')
            price_list.append(price)
            img_url = product_detail.get_attribute('src-webp')
            img_list.append(img_url)

            idx += 1

        # 商品名と価格を商品ごとに結合
        idx_name_price_img = list(zip(idx_list, name_list, price_list, img_list))

        return idx_name_price_img
