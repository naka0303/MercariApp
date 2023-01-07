import datetime
import socket
import time
import tkinter as tk
import traceback
import sys
import os
# os.chdir('../../')
# sys.path.append(os.getcwd() + '/py/loggings/')
# sys.path.append(os.getcwd() + '/py/dating/')
import log_outputter
import date_formatter


class StartView:
    """
    検索文字列入力フォーム用クラス

    """

    ### 変数宣言 ###
    # 現在時刻取得
    DT_NOW = datetime.datetime.now()

    # 各ディレクトリパス格納
    os.chdir('../../')
    APP_DIR_PATH = os.getcwd()
    SRC_DIR_PATH = APP_DIR_PATH + '/src'
    LOGS_DIR_PATH = APP_DIR_PATH + '/logs/py'
    TMP_DIR_PATH = APP_DIR_PATH + '/tmp'
    
    # 実行ファイル名取得
    RUN_FILENAME = os.path.basename(__file__)

    def __init__(self):
        ### インスタンス生成 ###
        self.log_outputter = log_outputter.LogOutputter(self.APP_DIR_PATH, self.LOGS_DIR_PATH, self.RUN_FILENAME)
        self.date_formatter = date_formatter.DateFormatter()

        self.root = ''
        self.search_word1 = ''
        self.search_word2 = ''
        self.search_word3 = ''
        self.var1 = ''
        self.var2 = ''

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
    
    def make_input_form(self, yyyymmdd, hhmmss):
        """
        検索文字列入力フォームを作成する

        """
        
        # tkinterクラス生成
        self.root = tk.Tk()

        # タイトル設定
        self.root.title('検索文字入力フォーム')

        # 画面の大きさ設定
        self.root.geometry('700x700')

        # 検索文字列入力欄生成
        label1 = tk.Label(text='■ 検索文字列')
        label1.place(x=30, y=40)
        label2 = tk.Label(text='検索文字列1:')
        label2.place(x=30, y=70)
        self.search_word1 = tk.Entry(width=20)
        self.search_word1.place(x=110, y=70)
        label3 = tk.Label(text='検索文字列2:')
        label3.place(x=30, y=100)
        self.search_word2 = tk.Entry(width=20)
        self.search_word2.place(x=110, y=100)
        label4 = tk.Label(text='検索文字列3:')
        label4.place(x=30, y=130)
        self.search_word3 = tk.Entry(width=20)
        self.search_word3.place(x=110, y=130)

        # 商品状況選択ラジオボタン生成
        label5 = tk.Label(text='■ 販売状況')
        label5.place(x=30, y=160)
        self.var1 = tk.IntVar(0)
        self.var1.set(0)
        status_btn1 = tk.Radiobutton(self.root, value=0, variable=self.var1, text='販売中')
        status_btn1.place(x=30, y=190)
        status_btn2 = tk.Radiobutton(self.root, value=1, variable=self.var1, text='売り切れ')
        status_btn2.place(x=150, y=190)

        # 並び替え選択ラジオボタン生成
        label6 = tk.Label(text='■ 販売状況')
        label6.place(x=30, y=220)
        self.var2 = tk.IntVar(0)
        self.var2.set(2)
        status_btn3 = tk.Radiobutton(self.root, value=2, variable=self.var2, text='新しい順')
        status_btn3.place(x=30, y=250)
        status_btn4 = tk.Radiobutton(self.root, value=3, variable=self.var2, text='おすすめ順')
        status_btn4.place(x=150, y=250)
        status_btn5 = tk.Radiobutton(self.root, value=4, variable=self.var2, text='価格の安い順')
        status_btn5.place(x=270, y=250)
        status_btn6 = tk.Radiobutton(self.root, value=5, variable=self.var2, text='価格の高い順')
        status_btn6.place(x=390, y=250)
        status_btn7 = tk.Radiobutton(self.root, value=6, variable=self.var2, text='いいね順')
        status_btn7.place(x=510, y=250)

        # 入力された情報をテキスト出力する
        search_btn = tk.Button(self.root, text='検索', command=self.output_search_condition)
        search_btn.place(x=140, y=280)

        self.root.mainloop()

    def output_search_condition(self):
        """
        検索文字列をテキストに出力する

        """

        search_words = [self.search_word1.get(), self.search_word2.get(), self.search_word3.get()]
        with open(self.TMP_DIR_PATH + '/' + yyyymmdd + '_' + hhmmss + '.txt', 'w') as f:
            for search_word in search_words:
                f.write(search_word + '\n')
            f.write(str(self.var1.get()) + '\n')
            f.write(str(self.var2.get()))

        self.end()

    def end(self):
        """
        ウィンドウの表示を終了する

        """

        self.root.destroy()

if __name__ == '__main__':
    try:
        # 処理時間計測開始
        START = time.perf_counter()

        # インスタンス生成
        start_view = StartView()

        start_view.output_log('========== START APP ==========')

        # 引数チェック
        args = sys.argv
        if (len(args) == 3):
            start_view.output_log('ARG1: ' + str(args[1]))
            start_view.output_log('ARG2: ' + str(args[2]))
        else:
            raise Exception

        # 引数セット
        yyyymmdd = args[1]
        hhmmss = args[2]

        start_view.output_log('RUNTIME: ' + str(start_view.DT_NOW))
        start_view.output_log('APP_DIR_PATH: ' + start_view.APP_DIR_PATH)
        start_view.output_log('SRC_DIR_PATH: ' + start_view.SRC_DIR_PATH)
        start_view.output_log('LOGS_DIR_PATH: ' + start_view.LOGS_DIR_PATH)
        start_view.output_log('TMP_DIR_PATH; ' + start_view.TMP_DIR_PATH)
        start_view.output_log('output_log_file: ' + start_view.LOGS_DIR_PATH + '/' + start_view.LOG_FILE)
    
        # 検索文字列入力フォームを作成する
        start_view.make_input_form(yyyymmdd, hhmmss)

        # 検索文字列をテキストに出力する
        # start_view.output_search_condition(yyyymmdd, hhmmss, var1, var2, search_word1, search_word2, search_word3)

        # ウィンドウの表示を終了する
        # start_view.end(self.root)

        # 処理時間計測終了
        END = time.perf_counter()

        # 処理時間計測
        process_time = start_view.calc_runtime(START, END)
        start_view.output_log('PROCESS_TIME: ' + str(process_time))

        # 処理正常終了
        start_view.output_log('========== NORMAL END ==========')

    except Exception:
        # 処理異常終了
        start_view.output_log('========== ABEND ==========')
        start_view.output_log('以下のエラーメッセージを確認')
        start_view.output_log(traceback.format_exc())
        start_view.output_log('===========================')
