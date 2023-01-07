import csv
import math
import matplotlib.pyplot as plt
import os
import sys
os.chdir('../../')
sys.path.append(os.getcwd() + '/py/loggings/')
sys.path.append(os.getcwd() + '/py/dating/')
import log_outputter
import date_formatter
import time
import datetime
import traceback


class MakeGraph:
    """
    グラフ作成用クラス
    """

    ### 変数宣言 ###
    # 現在時刻取得
    DT_NOW = datetime.datetime.now()

    # 各ディレクトリパス格納
    os.chdir('../')
    APP_DIR_PATH = os.getcwd()
    SRC_DIR_PATH = APP_DIR_PATH + '/src'
    CSV_DIR_PATH = APP_DIR_PATH + '/csv'
    LOGS_DIR_PATH = APP_DIR_PATH + '/logs'
    GRAPH_DIR_PATH = APP_DIR_PATH + '/graph'

    # 実行ファイル名取得
    RUN_FILENAME = os.path.basename(__file__)

    def __init__(self):
        ### インスタンス生成 ###
        self.log_outputter = log_outputter.LogOutputter(self.APP_DIR_PATH, self.LOGS_DIR_PATH, self.RUN_FILENAME)
        self.date_formatter = date_formatter.DateFormatter()

        # 日時のフォーマットを任意の形式に変更
        self.yyyymmdd, self.yyyymmddhhmmss = self.date_formatter.format_date()

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

    def make_price_list(self, csv_file):
        """
        CSVファイルから、価格の昇順にした配列を作成する
        """

        prices = []
        with open(csv_file + '.csv', 'r') as f:
            reader = csv.reader(f)
            for r in reader:
                prices.append(int(r[2]))
        
        prices_sorted = sorted(prices)

        return prices_sorted

    def get_price_diff(self, prices_sorted):
        """
        昇順にした価格リストから、最低価格と最高価格を取得した後、
        最高価格と最低価格の差を取得する
        """

        # 昇順にした価格リストから、最低価格と最高価格を取得する
        price_min = prices_sorted[0]
        price_max = prices_sorted[-1]

        # 最高価格と最低価格の差を取得する
        price_diff = price_max - price_min

        return price_diff

    def split_price_list(self, price_diff, prices_sorted):
        """
        価格リストを決定された価格ごとに分割する
        """

        # 横軸を10個にできるよう以下のように価格の分け方を決定する
        price_range = [math.floor(i * (price_diff / 10)) for i in range(10)]

        ## 決定された価格分割に沿って、価格リストを分割していく
        item_num_list = []
        for i in range(len(price_range)):
            if i == 0:
                item_num = len([price for price in prices_sorted if price < price_range[i+1]])
                item_num_list.append(item_num)
            elif i == 9:
                item_num = len([price for price in prices_sorted if price_range[i] <= price])
                item_num_list.append(item_num)
            else:
                item_num = len([price for price in prices_sorted if price_range[i] <= price and price < price_range[i+1]])
                item_num_list.append(item_num)

        return [price_range, item_num_list]
    
    def make_bar_graph(self, price_range, item_num_list):
        """
        価格と件数の棒グラフを作成する
        """

        # グラフの横軸（価格帯）
        left = price_range
        # グラフの縦軸（件数）
        height = item_num_list

        label = [str(price) + 'yen~' for price in price_range]

        plt.figure(figsize=(13, 5))
        plt.bar(left, height, tick_label=label, edgecolor='blue', linewidth=100, align='center', width=1)
        plt.xlabel('Price Range')
        plt.ylabel('Item Num')

        arg_splited = args[1].split('/')
        jpeg_file = self.GRAPH_DIR_PATH + '/' + arg_splited[-1] + '.jpeg'
        plt.savefig(jpeg_file)

if __name__ == '__main__':
    try:
        # 処理時間計測開始
        START = time.perf_counter()

        # インスタンス生成
        make_graph = MakeGraph()

        make_graph.output_log('========== START APP ==========')

        # 引数チェック
        args = sys.argv
        if (len(args) == 2):
            make_graph.output_log('ARG1: ' + str(args[1]))
        else:
            raise Exception

        # 引数セット
        csv_file = args[1]

        make_graph.output_log('RUNTIME: ' + str(make_graph.DT_NOW))
        make_graph.output_log('APP_DIR_PATH: ' + make_graph.APP_DIR_PATH)
        make_graph.output_log('SRC_DIR_PATH: ' + make_graph.SRC_DIR_PATH)
        make_graph.output_log('CSV_DIR_PATH: ' + make_graph.CSV_DIR_PATH)
        make_graph.output_log('LOGS_DIR_PATH: ' + make_graph.LOGS_DIR_PATH)
        make_graph.output_log('GRAPH_DIR_PATH: ' + make_graph.GRAPH_DIR_PATH)
        make_graph.output_log('OUTPUT_LOG_PATH: ' + make_graph.LOGS_DIR_PATH + '/' + make_graph.LOG_FILE)

        # CSVファイルから、価格の昇順にした配列を作成する
        prices_sorted = make_graph.make_price_list(csv_file)

        # 昇順にした価格リストから、最低価格と最高価格を取得した後、最高価格と最低価格の差を取得する
        price_diff = make_graph.get_price_diff(prices_sorted)

        # 価格リストを決定された価格ごとに分割する
        price_range, item_num_list = make_graph.split_price_list(price_diff, prices_sorted)

        # 価格と件数の棒グラフを作成する
        make_graph.make_bar_graph(price_range, item_num_list)

        # 処理時間計測終了
        END = time.perf_counter()

        # 処理時間計測
        process_time = make_graph.calc_runtime(START, END)
        make_graph.output_log('PROCESS_TIME: ' + str(process_time))

        # 処理正常終了
        make_graph.output_log('========== NORMAL END ==========')
    
    except Exception:
        # 処理異常終了
        make_graph.output_log('========== ABEND ==========')
        make_graph.output_log('以下のエラーメッセージを確認')
        make_graph.output_log(traceback.format_exc())
        make_graph.output_log('===========================')
