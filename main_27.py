import tkinter as tk
from tkinter import ttk
from func_27 import load, check, payments

def main():
    root = tk.Tk()
    root.title("газета")
    root.geometry("600x400")

    btn_frame = tk.Frame()
    btn_frame.pack()

    tk.Button(btn_frame, text="Статьи на рассмотрении на дату", command = check).grid(row=0, column=0, padx=20, pady=20)
    tk.Button(btn_frame, text="Таблица выплат за период", command=payments).grid(row=0, column=1, padx=20, pady=20)

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


