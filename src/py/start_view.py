import time
import tkinter as tk
import traceback
import sys
import os
os.chdir('../../')
sys.path.append(os.getcwd() + '/settings/')
import settings
import log_outputter
import date_formatter


class StartView:
    """
    検索文字列入力フォーム用クラス

    """

    ### 変数宣言 ###
    # 現在時刻取得
    DT_NOW = settings.DT_NOW

    # 要素探索待機時間
    SLEEP_TIME = settings.SLEEP_TIME

    # 実行ホスト
    HOSTNAME = settings.HOSTNAME

    # 各ディレクトリパス
    APP_DIR_PATH = settings.APP_DIR_PATH
    SRC_DIR_PATH = settings.SRC_DIR_PATH
    PY_LOGS_DIR_PATH = settings.PY_LOGS_DIR_PATH
    TMP_DIR_PATH = settings.TMP_DIR_PATH
    
    # 実行ファイル名
    RUN_FILENAME = os.path.basename(__file__)

    def __init__(self):
        ### インスタンス生成 ###
        self.log_outputter = log_outputter.LogOutputter(self.APP_DIR_PATH, self.PY_LOGS_DIR_PATH, self.RUN_FILENAME)
        self.date_formatter = date_formatter.DateFormatter()

        self.root = ''
        self.search_word1 = ''
        self.search_word2 = ''
        self.search_word3 = ''
        self.var1 = ''
        self.var2 = ''

        # 引数
        self.args = ''

        # 日時のフォーマットを任意の形式に変更
        self.yyyymmdd, self.yyyymmddhhmmss = self.date_formatter.format_date()

        # ログファイル名
        self.LOG_FILE = self.yyyymmdd + '_' + self.RUN_FILENAME + '_log.txt'

        # 空のログファイルをlogsディレクトリ下に生成
        self.log_outputter.make_logfile(self.LOG_FILE)

    def check_args(self):
        """
        引数を確認する

        """
        input_args = sys.argv

        if len(input_args) != 3:
            raise Exception
        
        self.args = input_args
        self.output_log('ARG1: ' + str(self.args[1]))
        self.output_log('ARG2: ' + str(self.args[2]))

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
    
    def make_input_form(self):
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
        label6 = tk.Label(text='■ 並び替え')
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
        search_btn = tk.Button(self.root, text='出力', command=self.output_search_condition)
        search_btn.place(x=140, y=280)

        self.root.mainloop()

    def output_search_condition(self):
        """
        検索文字列をテキストに出力する

        """

        l_search_word1 = self.search_word1.get()
        l_search_word2 = self.search_word2.get()
        l_search_word3 = self.search_word3.get()
        search_words = [l_search_word1, l_search_word2, l_search_word3]

        yyyymmdd = str(self.args[1])
        hhmmss = str(self.args[2])

        with open(self.TMP_DIR_PATH + '/' + yyyymmdd + '_' + hhmmss + '.txt', 'w') as f:
            f.write('検索ワード1 ' + '検索ワード2 ' + '検索ワード3 ' + '販売状況 ' + '並び替え' + '\n')
            for search_word in search_words:
                if len(search_word) != 0:
                    f.write(search_word + ' ')
                else:
                    f.write('None' + ' ')
            f.write(str(self.var1.get()) + ' ' + str(self.var2.get()))

        self.end()

    def end(self):
        """
        ウィンドウの表示を終了する

        """

        self.root.destroy()

    def main():
        try:
            # 処理時間計測開始
            START = time.perf_counter()

            # インスタンス生成
            start_view = StartView()

            start_view.output_log('========== START APP ==========')

            # 引数チェック
            start_view.check_args()

            start_view.output_log('RUNTIME: ' + str(start_view.DT_NOW))
            start_view.output_log('APP_DIR_PATH: ' + start_view.APP_DIR_PATH)
            start_view.output_log('SRC_DIR_PATH: ' + start_view.SRC_DIR_PATH)
            start_view.output_log('PY_LOGS_DIR_PATH: ' + start_view.PY_LOGS_DIR_PATH)
            start_view.output_log('TMP_DIR_PATH; ' + start_view.TMP_DIR_PATH)
            start_view.output_log('output_log_file: ' + start_view.PY_LOGS_DIR_PATH + '/' + start_view.LOG_FILE)
        
            # 検索文字列入力フォームを作成する
            start_view.make_input_form()

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

if __name__ == '__main__':
    StartView.main()