import datetime
import os
import socket
import sys
import time
import traceback
import log_outputter
import date_formatter
import csv_filer
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options

class Scrape:
    """
    商品情報取得用クラス
    """

    ### 変数宣言 ###
    # 現在時刻取得
    DT_NOW = datetime.datetime.now()

    # スクレイピング時の要素探索最大待機時間
    SLEEP_TIME = 60

    # 実行ホスト確認
    HOSTNAME = socket.gethostname()

    # 各ディレクトリパス格納
    os.chdir('../../')
    APP_DIR_PATH = os.getcwd()
    CSV_DIR_PATH = APP_DIR_PATH + '/csv'
    LOGS_DIR_PATH = APP_DIR_PATH + '/logs/py'

    # 実行ファイル名取得
    RUN_FILENAME = os.path.basename(__file__)

    # コンストラクタ
    def __init__(self):
        ### インスタンス生成 ###
        self.log_outputter = log_outputter.LogOutputter(self.APP_DIR_PATH, self.LOGS_DIR_PATH, self.RUN_FILENAME)
        self.date_formatter = date_formatter.DateFormatter()
        self.csv_filer = csv_filer.CsvFiler()

        # 日時のフォーマットを任意の形式に変更
        self.yyyymmdd, self.yyyymmddhhmmss = self.date_formatter.format_date()

        # 商品情報出力用csvファイル名
        self.all_product_csv_file = self.yyyymmddhhmmss + '_all_product.csv'

        # ログファイル名
        self.LOG_FILE = self.yyyymmdd + '_' + self.RUN_FILENAME + '_log.txt'

        # 空のログファイルをlogsディレクトリ下に生成
        self.log_outputter.make_logfile(self.LOG_FILE)

    def calc_runtime(self, start, end):
        """
        処理時間を計測する

        """

        process_time = end - start
        
        return process_time

    def output_log(self, msg):
        """
        ログをテキスト出力する

        """

        self.log_outputter.info(msg, self.LOG_FILE)

    def output_csv(self, name_price_img, search_word1, search_word2, search_word3):
        """
        CSVに商品情報を出力する
        
        """
        
        search_words = [search_word1, search_word2, search_word3]

        # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
        all_name_price_img_removed = self.csv_filer.remove_unneeded(search_words[0:], name_price_img)
        self.log_outputter.info('PRODUCT_COUNT: ' + str(len(all_name_price_img_removed)), self.LOG_FILE)

        # 全商品情報をcsvに出力
        self.csv_filer.write_data(self.CSV_DIR_PATH, self.all_product_csv_file, all_name_price_img_removed, 'w')

        # スプレッドシート書き込み
        # spreadsheeter.make_sheet(OAUTH_DIR_PATH, yyyymmddhhmmss, all_idx_name_price_img_removed)

    def make_url(self, search_word1, search_word2, search_word3, status, sort_order, page_num):
        """
        メルカリURL作成

        """
        
        # ページ番号
        page_num = str(page_num)

        # 検索ワード
        search_words = '%20'.join([w for w in [search_word1, search_word2, search_word3] if w != 'None'])

        # 販売状況
        # - 販売中 : status=on_sale
        # - 売り切れ : status=sold_out
        status_str = 'status=on_sale' if status == '0' else 'status=sold_out'
    
        # 並び替え
        # - 新しい順 : order=desc&sort=created_time
        # - おすすめ順 : sort=score&order=desc
        # - 価格の安い順 : order=asc&sort=price
        # - 価格の高い順 : sort=price&order=desc
        # - いいね順 : order=desc&sort=num_likes
        sort_order_str = ''
        if sort_order == '2':
            sort_order_str = 'sort=score&order=desc'
        elif sort_order == '3':
            sort_order_str = 'sort=score&order=desc'
        elif sort_order == '4':
            sort_order_str = 'order=asc&sort=price'
        elif sort_order == '5':
            sort_order_str = 'sort=price&order=desc'
        else:
            sort_order_str = 'order=desc&sort=num_likes'
        
        self.output_log('PAGE_NUM: ' + page_num)
        self.output_log('SEARCH_WORD: ' + search_words)
        self.output_log('STATUS: ' + status_str)
        self.output_log('SORT_ORDER: ' + sort_order_str)

        mercari_url = "https://jp.mercari.com/search?keyword=" + search_words + "&" + sort_order_str + "&" + status_str + "&page_token=v1%3A" + page_num

        return mercari_url

    def run(self, driver, search_word1, search_word2, search_word3, mercari_url):
        """
        メルカリ画面のスクレイピング実行

        """

        # メルカリ公式サイトを開く
        driver.get(mercari_url)

        # 出品商品情報取得
        driver.implicitly_wait(self.SLEEP_TIME)
        products = driver.find_element(By.XPATH, '//*[@id="item-grid"]/ul')

        driver.implicitly_wait(self.SLEEP_TIME)
        products_div = products.find_elements(By.TAG_NAME, 'div')

        # 商品ごとに、商品名と価格と画像URLを取得する
        name_list = []
        price_list = []
        img_list = []
        for product in products_div:
            product_detail = product.find_element(By.TAG_NAME, 'mer-item-thumbnail')

            name = product_detail.get_attribute('alt')
            name_removed = name.replace('のサムネイル', '')
            name_list.append(name_removed)
            price = product_detail.get_attribute('price')
            price_list.append(price)
            img_url = product_detail.get_attribute('src-webp')
            img_list.append(img_url)

        # 商品名と価格を商品ごとに結合
        name_price_img = list(zip(name_list, price_list, img_list))

        search_words = [w for w in [search_word1, search_word2, search_word3] if w != 'None']

        # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
        name_price_img_removed = self.csv_filer.remove_unneeded(search_words[0:], name_price_img)
        self.log_outputter.info('PRODUCT_COUNT: ' + str(len(name_price_img_removed)), self.LOG_FILE)

        # 全商品情報をcsvに出力
        self.csv_filer.write_data(self.CSV_DIR_PATH, self.all_product_csv_file, name_price_img_removed, 'a')

    def main():
        try:
            # 処理時間計測開始
            START = time.perf_counter()

            # インスタンス生成
            scrape = Scrape()

            scrape.output_log('========== START APP ==========')

            # 引数チェック
            args = sys.argv

            if (len(args) == 6):
                scrape.output_log('ARG1: ' + str(args[1]))
                scrape.output_log('ARG2: ' + str(args[2]))
                scrape.output_log('ARG3: ' + str(args[3]))
                scrape.output_log('ARG4: ' + str(args[4]))
                scrape.output_log('ARG5: ' + str(args[5]))
            else:
                raise Exception

            # 引数セット
            search_word1 = str(args[1])
            search_word2 = str(args[2])
            search_word3 = str(args[3])
            status = str(args[4])
            sort_order = str(args[5])

            scrape.output_log('RUNTIME: ' + str(scrape.DT_NOW))
            scrape.output_log('HOSTNAME: ' + scrape.HOSTNAME)
            scrape.output_log('APP_DIR_PATH: ' + scrape.APP_DIR_PATH)
            scrape.output_log('LOGS_DIR_PATH: ' + scrape.LOGS_DIR_PATH)
            scrape.output_log('OUTPUT_LOG_PATH: ' + scrape.LOGS_DIR_PATH + '/' + scrape.LOG_FILE)

            driver_dir_path = ''
            options = Options()
            options.headless = True
            if ('local' in scrape.HOSTNAME):
                # FIXME: chromedriverに更新があれば自動で更新できるようにする
                # chromedriverパス格納
                driver_dir_path = scrape.APP_DIR_PATH + '/driver'
                DRIVER_PATH = fs.Service(executable_path=driver_dir_path + '/chromedriver')
                driver = webdriver.Chrome(service=DRIVER_PATH, options=options)
            else:
                import chromedriver_binary
                driver = webdriver.Chrome(options=options)

            for page_num in range(3):
                # メルカリURL作成
                mercari_url = scrape.make_url(search_word1, search_word2, search_word3, status, sort_order, page_num)

                # メルカリ画面のスクレイピング実行
                scrape.run(driver, search_word1, search_word2, search_word3, mercari_url)

            driver.close()

            # 処理時間計測終了
            END = time.perf_counter()

            # 処理時間計測
            process_time = scrape.calc_runtime(START, END)
            scrape.output_log('PROCESS_TIME: ' + str(process_time))

            # 処理正常終了
            scrape.output_log('========== NORMAL END ==========')

        except Exception:
            # 処理異常終了
            scrape.output_log('========== ABEND ==========')
            scrape.output_log('以下のエラーメッセージを確認')
            scrape.output_log(traceback.format_exc())
            scrape.output_log('===========================')

if __name__ == '__main__':
    Scrape.main()
