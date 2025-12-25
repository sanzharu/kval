import pymysql
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import os


class DatabaseManager:
    def __init__(self, use_csv=False):
        self.use_csv = use_csv

    def connect_db(self):
        if self.use_csv:
            print("Using CSV files for testing")
            return None

        try:
            db = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                database='autovoksal'
            )
            print("Successful db connection")
            return db
        except Exception as e:
            print(f"NOT {e}")
            return None


class CSVDataManager:
    def __init__(self):
        self.data_dir = "csv_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.setup_csv_files()

    def setup_csv_files(self):
        # Файл с автобусами
        bus_file = os.path.join(self.data_dir, "bus.csv")
        if not os.path.exists(bus_file):
            bus_data = [
                ["Bus id", "Mark bus", "Gos number", "Vmest"],
                [1, "Mercedes", "A123BC", 50],
                [2, "Volvo", "B456DE", 45],
                [3, "MAN", "C789FG", 55],
                [4, "Scania", "D012HI", 60],
                [5, "Mercedes", "E345JK", 40]
            ]
            self.write_csv(bus_file, bus_data)

        # Файл с рейсами
        race_file = os.path.join(self.data_dir, "race.csv")
        if not os.path.exists(race_file):
            race_data = [
                ["race_id", "bus_id", "station_id"],
                [1, 1, 101],
                [2, 2, 101],
                [3, 3, 102],
                [4, 1, 102],
                [5, 4, 103],
                [6, 5, 101],
                [7, 2, 103]
            ]
            self.write_csv(race_file, race_data)

    def write_csv(self, filename, data):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def read_csv(self, filename):
        data = []
        if os.path.exists(filename):
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
        return data

    def get_bus_data(self):
        bus_file = os.path.join(self.data_dir, "bus.csv")
        return self.read_csv(bus_file)[1:]  # Пропускаем заголовок

    def get_race_data(self):
        race_file = os.path.join(self.data_dir, "race.csv")
        return self.read_csv(race_file)[1:]  # Пропускаем заголовок


class MainWindow:
    def __init__(self, use_csv=False):
        self.root = tk.Tk()
        self.root.title("System")
        self.root.geometry("1000x600")

        self.use_csv = use_csv
        self.db_manager = DatabaseManager(use_csv)
        if use_csv:
            self.csv_manager = CSVDataManager()

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
        if self.use_csv:
            # Загрузка из CSV
            bus_data = self.csv_manager.get_bus_data()
            for row in bus_data:
                self.tree.insert("", "end", values=row)
        else:
            # Загрузка из базы данных
            db = self.db_manager.connect_db()
            if db:
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

        if self.use_csv:
            # Обработка из CSV
            race_data = self.csv_manager.get_race_data()

            # Группировка по station_id
            station_counts = {}
            for row in race_data:
                station_id = int(row[2])
                station_counts[station_id] = station_counts.get(station_id, 0) + 1

            columns = ["Station id", "Total"]
            tree1 = ttk.Treeview(tree_frame, columns=columns, show="headings")
            for col in columns:
                tree1.heading(col, text=col)

            with open("sort.txt", 'w') as f:
                f.write("\t".join(columns) + "\n")

                for station_id, count in station_counts.items():
                    tree1.insert("", "end", values=[station_id, count])
                    f.write(f"{station_id}\t{count}\n")
        else:
            # Обработка из базы данных
            db = self.db_manager.connect_db()
            if db:
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

        if self.use_csv:
            # Обработка из CSV
            bus_data = self.csv_manager.get_bus_data()

            # Группировка по марке автобуса
            mark_totals = {}
            for row in bus_data:
                mark_bus = row[1]
                gos_number = row[2]
                vmest = int(row[3])

                key = (mark_bus, gos_number)
                mark_totals[key] = mark_totals.get(key, 0) + vmest

            columns = ["Mark bus", "Gos number", "Total"]
            tree2 = ttk.Treeview(tree_frame, columns=columns, show="headings")
            for col in columns:
                tree2.heading(col, text=col)

            with open("alpha.txt", 'w') as f:
                f.write("\t".join(columns) + "\n")

                for (mark_bus, gos_number), total in mark_totals.items():
                    tree2.insert("", "end", values=[mark_bus, gos_number, total])
                    f.write(f"{mark_bus}\t{gos_number}\t{total}\n")
        else:
            # Обработка из базы данных
            db = self.db_manager.connect_db()
            if db:
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
    # Спросить пользователя, использовать ли CSV файлы
    use_csv = messagebox.askyesno("Режим работы",
                                  "Использовать CSV файлы для тестирования?\n\n"
                                  "ДА - использовать тестовые CSV файлы\n"
                                  "НЕТ - использовать базу данных")

    app = MainWindow(use_csv=use_csv)
    app.run()


if __name__ == "__main__":
    main()