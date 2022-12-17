import datetime
import socket
import time
import tkinter as tk
import traceback
import sys
import os
os.chdir('../../')
sys.path.append(os.getcwd() + '/py/loggings/')
sys.path.append(os.getcwd() + '/py/dating/')
import log_outputter
import date_formatter


class StartView:
    """
    検索文字列入力フォーム用クラス

    (1) 検索文字列入力フォームを作成する
    (2) (1)で入力された情報をテキスト出力する

    """
    ### 変数宣言 ###
    # 処理開始時刻
    START = time.perf_counter()

    # 現在時刻
    DT_NOW = datetime.datetime.now()

    # 実行ホスト
    hostname = socket.gethostname()

    # 各ディレクトリパス
    os.chdir('../')
    APP_DIR_PATH = os.getcwd()
    SRC_DIR_PATH = APP_DIR_PATH + '/src'
    LOGS_DIR_PATH = APP_DIR_PATH + '/logs'
    TMP_DIR_PATH = APP_DIR_PATH + '/tmp'

    # 実行ファイル名
    RUN_FILENAME = os.path.basename(__file__)

    ### インスタンス生成 ###
    log_outputter = log_outputter.LogOutputter(APP_DIR_PATH, LOGS_DIR_PATH, RUN_FILENAME)
    date_formatter = date_formatter.DateFormatter()

    # 日時のフォーマットを任意の形式に変更
    yyyymmdd, yyyymmddhhmmss = date_formatter.format_date()

    # ログファイル名
    LOG_FILE = yyyymmdd + '_' + RUN_FILENAME + '_log.txt'

    # 空のログファイルをlogsディレクトリ下に生成
    log_outputter.make_logfile(LOG_FILE)

    ### 変数確認 ###
    log_outputter.info('========== START APP ==========', LOG_FILE)
    log_outputter.info('RUNTIME: ' + str(DT_NOW), LOG_FILE)
    log_outputter.info('APP_DIR_PATH: ' + APP_DIR_PATH, LOG_FILE)
    log_outputter.info('SRC_DIR_PATH: ' + SRC_DIR_PATH, LOG_FILE)
    log_outputter.info('LOGS_DIR_PATH: ' + LOGS_DIR_PATH, LOG_FILE)
    log_outputter.info('TMP_DIR_PATH; ' + TMP_DIR_PATH, LOG_FILE)
    log_outputter.info('output_log_file: ' + LOGS_DIR_PATH + '/' + LOG_FILE, LOG_FILE)

    def __init__(self, yyyymmdd, hhmmss):
        try:
            ### 引数取得 ###
            self.yyyymmdd = yyyymmdd
            self.hhmmss = hhmmss

            ### 引数確認 ###
            self.log_outputter.info('yyyymmdd: ' + str(yyyymmdd), self.LOG_FILE)
            self.log_outputter.info('hhmmss: ' + str(hhmmss), self.LOG_FILE)

            ### (1) 検索文字列入力フォームを作成する ###
            # tkinterクラス生成
            self.root = tk.Tk()

            # タイトル設定
            self.root.title('検索文字入力フォーム')

            # 画面の大きさ設定
            self.root.geometry('700x700')

            # 検索文字列入力欄生成
            self.label1 = tk.Label(text='■ 検索文字列')
            self.label1.place(x=30, y=40)
            self.label2 = tk.Label(text='検索文字列1:')
            self.label2.place(x=30, y=70)
            self.search_word1 = tk.Entry(width=20)
            self.search_word1.place(x=110, y=70)
            self.label3 = tk.Label(text='検索文字列2:')
            self.label3.place(x=30, y=100)
            self.search_word2 = tk.Entry(width=20)
            self.search_word2.place(x=110, y=100)
            self.label4 = tk.Label(text='検索文字列3:')
            self.label4.place(x=30, y=130)
            self.search_word3 = tk.Entry(width=20)
            self.search_word3.place(x=110, y=130)

            # 商品状況選択ラジオボタン生成
            self.label5 = tk.Label(text='■ 販売状況')
            self.label5.place(x=30, y=160)
            self.var1 = tk.IntVar(0)
            self.var1.set(0)
            self.status_btn1 = tk.Radiobutton(self.root, value=0, variable=self.var1, text='販売中')
            self.status_btn1.place(x=30, y=190)
            self.status_btn2 = tk.Radiobutton(self.root, value=1, variable=self.var1, text='売り切れ')
            self.status_btn2.place(x=150, y=190)

            # 並び替え選択ラジオボタン生成
            self.label6 = tk.Label(text='■ 販売状況')
            self.label6.place(x=30, y=220)
            self.var2 = tk.IntVar(0)
            self.var2.set(2)
            self.status_btn3 = tk.Radiobutton(self.root, value=2, variable=self.var2, text='新しい順')
            self.status_btn3.place(x=30, y=250)
            self.status_btn4 = tk.Radiobutton(self.root, value=3, variable=self.var2, text='おすすめ順')
            self.status_btn4.place(x=150, y=250)
            self.status_btn5 = tk.Radiobutton(self.root, value=4, variable=self.var2, text='価格の安い順')
            self.status_btn5.place(x=270, y=250)
            self.status_btn6 = tk.Radiobutton(self.root, value=5, variable=self.var2, text='価格の高い順')
            self.status_btn6.place(x=390, y=250)
            self.status_btn7 = tk.Radiobutton(self.root, value=6, variable=self.var2, text='いいね順')
            self.status_btn7.place(x=510, y=250)

            ### (2) (1)で入力された情報をテキスト出力する ###
            self.search_btn = tk.Button(self.root, text='検索', command=self.output_search_condition)
            self.search_btn.place(x=140, y=280)

            self.root.mainloop()

        except Exception:
            self.log_outputter.error(traceback.format_exc(), self.LOG_FILE)
            self.log_outputter.error('========== ABEND ==========', self.LOG_FILE)

    def output_search_condition(self):
        """
        検索文字列のテキスト出力用関数
        
        """
        search_words = [self.search_word1.get(), self.search_word2.get(), self.search_word3.get()]
        with open(self.TMP_DIR_PATH + '/' + self.yyyymmdd + '_' + self.hhmmss + '.txt', 'w') as f:
            for search_word in search_words:
                f.write(search_word + '\n')
            f.write(str(self.var1.get()) + '\n')
            f.write(str(self.var2.get()))

        self.end()
    
    # ウィンドウの表示開始用関数
    def start(self):
        self.root.mainloop()

    # ウィンドウの表示終了用関数
    def end(self):
        self.root.destroy()

if __name__ == '__main__':
    ### 引数取得 ###
    args = sys.argv
    yyyymmdd = args[1]
    hhmmss = args[2]

    StartView(yyyymmdd, hhmmss)
