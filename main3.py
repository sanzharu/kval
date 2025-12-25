import pymysql
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='root', database='autovoksal'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect_db(self):
        try:
            db = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Successful db connection")
            return db
        except Exception as e:
            print(f"Connection error: {e}")
            return None


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("System")
        self.root.geometry("1000x600")

        self.db_manager = DatabaseManager()

    def create_widgets(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Рейсы до станции", command=self.sort).grid(row=0, column=0, pady=20)
        tk.Button(btn_frame, text="Общее количество пассажиров", command=self.alpha).grid(row=0, column=1, pady=20)

        tree_frame = tk.Frame(self.root)
        tree_frame.pack()

        columns = ["Bus id", "Mark bus", "Gos number", "Vmest"]
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack()

    def load(self):
        db = self.db_manager.connect_db()
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM autovoksal.bus;""")

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        db.close()

    def sort(self):
        add_win = tk.Toplevel()
        add_win.title("System")
        add_win.geometry("700x300")

        tree_frame = tk.Frame(add_win)
        tree_frame.pack()

        db = self.db_manager.connect_db()
        cursor = db.cursor()
        cursor.execute("""select r.station_id, count(bus_id) as total_race
from race r
group by r.station_id""")

        columns = ["Station id", "Total"]
        tree1 = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree1.heading(col, text=col)
        with open("sort.txt", 'w') as f:
            f.write("\t".join(columns) + "\n")

            for row in cursor.fetchall():
                tree1.insert("", "end", values=row)
                f.write("\t".join(str(item) for item in row) + "\n")

        tree1.pack()

    def alpha(self):
        add_win = tk.Toplevel()
        add_win.title("system")
        add_win.geometry("500x500")

        tree_frame = tk.Frame(add_win)
        tree_frame.pack()

        db = self.db_manager.connect_db()
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

    def run(self):
        self.create_widgets()
        self.load()
        self.root.mainloop()


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()