import csv
import math
import matplotlib.pyplot as plt
import os
import sys
os.chdir('../../')
sys.path.append(os.getcwd() + '/settings/')
import settings
import log_outputter
import date_formatter
import time
import traceback


class MakeGraph:
    """
    グラフ作成用クラス
    """

    ### 変数宣言 ###
    # 現在時刻取得
    DT_NOW = settings.DT_NOW

    # 各ディレクトリパス格納
    APP_DIR_PATH = settings.APP_DIR_PATH
    SRC_DIR_PATH = settings.SRC_DIR_PATH
    CSV_DIR_PATH = settings.CSV_DIR_PATH
    PY_LOGS_DIR_PATH = settings.PY_LOGS_DIR_PATH
    GRAPH_DIR_PATH = settings.GRAPH_DIR_PATH

    # 実行ファイル名取得
    RUN_FILENAME = os.path.basename(__file__)

    def __init__(self):
        ### インスタンス生成 ###
        self.log_outputter = log_outputter.LogOutputter(self.APP_DIR_PATH, self.PY_LOGS_DIR_PATH, self.RUN_FILENAME)
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
                prices.append(int(r[1]))
        
        prices_sorted = sorted(prices)

        return prices_sorted

    def make_bar_graph(self, prices_sorted, csv_file):
        """
        価格と件数の棒グラフを作成する
        """

        # 最大価格取得
        max_price = prices_sorted[-1]

        # 横軸の価格帯を設定
        plt.xlim(0, max_price)

        plt.grid(True)
        plt.hist(prices_sorted, alpha=1.0, bins=10)
        plt.xlabel('Price Range')
        plt.ylabel('Item Num')

        # graphディレクトリ下にjpegを保存
        arg_splited = csv_file.split('/')
        jpeg_file = self.GRAPH_DIR_PATH + '/' + arg_splited[-1] + '.jpeg'
        plt.savefig(jpeg_file)
    
    def main():
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
            make_graph.output_log('PY_LOGS_DIR_PATH: ' + make_graph.PY_LOGS_DIR_PATH)
            make_graph.output_log('GRAPH_DIR_PATH: ' + make_graph.GRAPH_DIR_PATH)
            make_graph.output_log('OUTPUT_LOG_PATH: ' + make_graph.PY_LOGS_DIR_PATH + '/' + make_graph.LOG_FILE)

            # CSVファイルから、価格の昇順にした配列を作成する
            prices_sorted = make_graph.make_price_list(csv_file)

            # 価格と件数の棒グラフを作成する
            make_graph.make_bar_graph(prices_sorted, csv_file)

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
    
if __name__ == '__main__':
    MakeGraph.main()
    