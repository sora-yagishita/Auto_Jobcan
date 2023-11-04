import tkinter as tk
import tkinter.ttk as ttk
from test.TestCase import TestCase

class Ui:

    def UiStart():
        root = tk.Tk()
        # rootメインウィンドウの設定
        root.attributes("-topmost", True)
        root.title("自動テストツール")
        root.geometry("420x300")

        # メインフレームの作成と設置
        frame = ttk.Frame(root)
        frame.pack(fill = tk.BOTH, padx=20,pady=10)

        # StringVarのインスタンスを格納する変数textの設定
        text = tk.StringVar(frame)
        test = TestCase()
        test.name = "テスト"
        text.set(test.name)

        # 各種ウィジェットの作成と設置
        button = tk.Button(root, textvariable=text)
        button.pack()

        root.mainloop()