import tkinter as tk

class StartView:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title('検索文字入力フォーム')
        self.root.geometry('500x500')

        self.label1 = tk.Label(text='検索文字列1:')
        self.label1.place(x=30, y=70)
        self.search_word1 = tk.Entry(width=10)
        self.search_word1.place(x=110, y=70)

        self.label2 = tk.Label(text='検索文字列2:')
        self.label2.place(x=30, y=100)
        self.search_word2 = tk.Entry(width=10)
        self.search_word2.place(x=110, y=100)

        self.label3 = tk.Label(text='検索文字列3:')
        self.label3.place(x=30, y=130)
        self.search_word3 = tk.Entry(width=10)
        self.search_word3.place(x=110, y=130)

        self.search_btn = tk.Button(self.root, text='検索', command=self.end)
        self.search_btn.place(x=140, y=170)

        self.root.mainloop()

    def get_search_word():
        search_word1 = search_word1.get()
        search_word2 = search_word2.get()
        search_word3 = search_word3.get()

    def start(self):
        # ウィンドウの表示開始
        self.root.mainloop()

    def end(self):
        # ウィンドウの表示終了
        self.root.destroy()

StartView()