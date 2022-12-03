import tkinter as tk
import sys
import os

# 検索文字列入力フォーム用クラス
class StartView:

    os.chdir('../../')
    APP_DIR_PATH = os.getcwd()
    TMP_DIR_PATH = APP_DIR_PATH + '/tmp'

    def __init__(self, yyyymmdd, hhmmss):
        # 引数取得
        self.yyyymmdd = yyyymmdd
        self.hhmmss = hhmmss

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

        # 検索ボタン生成
        self.search_btn = tk.Button(self.root, text='検索', command=self.output_search_word)
        self.search_btn.place(x=140, y=280)

        self.root.mainloop()

    # 検索文字列のテキスト出力用関数
    def output_search_word(self):
        search_words = [self.search_word1.get(), self.search_word2.get(), self.search_word3.get()]
        with open(self.TMP_DIR_PATH + '/' + self.yyyymmdd + '_' + self.hhmmss + '.txt', 'w') as f:
            for search_word in search_words:
                f.write('%s\n' % search_word)
            f.write(str(self.var1.get()))
            f.write(str(self.var2.get()))

        self.end()
    
    # ウィンドウの表示開始用関数
    def start(self):
        self.root.mainloop()

    # ウィンドウの表示終了用関数
    def end(self):
        self.root.destroy()

if __name__ == '__main__':
    # 引数取得
    args = sys.argv
    yyyymmdd = args[1]
    hhmmss = args[2]

    StartView(yyyymmdd, hhmmss)
