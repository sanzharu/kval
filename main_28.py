import mysql.connector as mc
import tkinter as tk
from tkinter import ttk, messagebox as mb
from datetime import datetime as dt
from func_28 import load, popular_docs, card_date

def main():
    root = tk.Tk()
    root.title("мфц")
    root.geometry("600x400")

    tk.Button(root, text="популярные документы", command=lambda: popular_docs(), width=25, height=2).pack(pady=20)
    tk.Button(root, text="дата получения карты",command=lambda: card_date(), width=25, height=2).pack(pady=20)

    tree_frame = tk.Frame()
    tree_frame.pack()
    columns = ["ID", "Название", "Фио"]
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)

    tree.pack()
    load(tree)
    root.mainloop()

if __name__ == "__main__":
    main()
