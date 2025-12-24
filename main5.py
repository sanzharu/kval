import pymysql
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

def connect_db():
    try:
        db = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='autovoksal'
        )
        print("Succeful db")
        return db
    except Exception as e:
        print(f"NOT {e}")

def main():
    root = tk.Tk()
    root.title("System")
    root.geometry("1000x600")

    btn_frame = tk.Frame()
    btn_frame.pack()

    tk.Button(btn_frame, text="Рейсы до станции", command=sort).grid(row=0, column=0, pady=20)
    tk.Button(btn_frame, text="Общее количество пассажиров", command=alpha).grid(row=0, column=1, pady=20)

    tree_frame = tk.Frame()
    tree_frame.pack()

    columns=["Bus id", "Mark bus", "Gos number", "Vmest"]
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)

    tree.pack()
    load(tree)
    root.mainloop()

def load(tree):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM autovoksal.bus;""")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    db.close()

def sort():
    add_win = tk.Toplevel()
    add_win.title("System")
    add_win.geometry("700x300")

    tree_frame = tk.Frame(add_win)
    tree_frame.pack()

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""select r.station_id, count(bus_id) as total_race
from race r
group by r.station_id""")

    columns=["Station id", "Total"]
    tree1 = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree1.heading(col, text=col)
    with open("sort.txt", 'w') as f:
        f.write("\t".join(columns) + "\n")

        for row in cursor.fetchall():
            tree1.insert("", "end", values=row)
            f.write("\t".join(str(item) for item in row) + "\n")

    tree1.pack()

def alpha():
    add_win = tk.Toplevel()
    add_win.title("system")
    add_win.geometry("500x500")

    tree_frame = tk.Frame(add_win)
    tree_frame.pack()

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""select r.mark_bus, r.gos_number, sum(r.vmest) as total
from bus r
group by r.vmest, r.mark_bus, r.gos_number""")

    columns = ["Mark bus", "Gos number"]
    tree2 = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree2.heading(col, text=col)
    with open("alpha.txt", 'w') as f:
        f.write("\t".join(columns) + "\n")

        for row in cursor.fetchall():
            tree2.insert("", "end", values=row)
            f.write("\t".join(str(item) for item in row) + "\n")

    tree2.pack()


if __name__ == "__main__":
    main()