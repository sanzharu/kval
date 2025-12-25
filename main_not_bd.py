import tkinter as tk
from tkinter import ttk
import csv
from database import CSVManager

class Application:
    def __init__(self, root):
        self.root = root
        self.csv_manager = CSVManager()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("System")
        self.root.geometry("1000x600")
        
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
        self.load_bus_data(self.tree)
        
    def load_bus_data(self, tree):
        try:
            with open('bus_data.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Пропускаем заголовок
                
                for row in csv_reader:
                    if len(row) >= 4:
                        tree.insert("", "end", values=row)
                        
        except Exception as e:
            print(f"Error loading bus data: {e}")
            
    def sort(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("System")
        add_win.geometry("700x300")
        
        tree_frame = tk.Frame(add_win)
        tree_frame.pack()
        
        try:
            # Читаем данные о рейсах из CSV файла
            station_data = {}
            with open('race_data.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Пропускаем заголовок
                
                for row in csv_reader:
                    if len(row) >= 4:
                        station_id = row[2]
                        if station_id in station_data:
                            station_data[station_id] += 1
                        else:
                            station_data[station_id] = 1
            
            columns = ["Station id", "Total"]
            tree1 = ttk.Treeview(tree_frame, columns=columns, show="headings")
            for col in columns:
                tree1.heading(col, text=col)
                
            with open("sort.txt", 'w', encoding='utf-8') as f:
                f.write("\t".join(columns) + "\n")
                
                for station_id, total in station_data.items():
                    row_data = [station_id, str(total)]
                    tree1.insert("", "end", values=row_data)
                    f.write("\t".join(row_data) + "\n")
                    
            tree1.pack()
            
        except Exception as e:
            print(f"Error in sort: {e}")
            
    def alpha(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("system")
        add_win.geometry("500x500")
        
        tree_frame = tk.Frame(add_win)
        tree_frame.pack()
        
        try:
            # Читаем данные об автобусах из CSV файла
            bus_passenger_data = {}
            with open('bus_data.csv', 'r', encoding='utf-8') as bus_file:
                bus_reader = csv.reader(bus_file)
                next(bus_reader)  # Пропускаем заголовок
                
                for row in bus_reader:
                    if len(row) >= 4:
                        bus_id = row[0]
                        bus_passenger_data[bus_id] = {
                            'mark_bus': row[1],
                            'gos_number': row[2],
                            'capacity': int(row[3])
                        }
            
            # Читаем данные о пассажирах из файла рейсов
            passenger_counts = {}
            with open('race_data.csv', 'r', encoding='utf-8') as race_file:
                race_reader = csv.reader(race_file)
                next(race_reader)  # Пропускаем заголовок
                
                for row in race_reader:
                    if len(row) >= 4:
                        bus_id = row[1]
                        passenger_count = int(row[3])
                        
                        if bus_id in passenger_counts:
                            passenger_counts[bus_id] += passenger_count
                        else:
                            passenger_counts[bus_id] = passenger_count
            
            columns = ["Mark bus", "Gos number", "Total"]
            tree2 = ttk.Treeview(tree_frame, columns=columns, show="headings")
            for col in columns:
                tree2.heading(col, text=col)
                
            with open("alpha.txt", 'w', encoding='utf-8') as f:
                f.write("\t".join(columns) + "\n")
                
                for bus_id, passenger_count in passenger_counts.items():
                    if bus_id in bus_passenger_data:
                        bus_info = bus_passenger_data[bus_id]
                        row_data = [
                            bus_info['mark_bus'],
                            bus_info['gos_number'],
                            str(passenger_count)
                        ]
                        tree2.insert("", "end", values=row_data)
                        f.write("\t".join(row_data) + "\n")
                    
            tree2.pack()
            
        except Exception as e:
            print(f"Error in alpha: {e}")

def main():
    root = tk.Tk()
    app = Application(root)
    
    # Создание CSV файлов с данными
    csv_manager = CSVManager()
    csv_manager.generate_bus_csv()
    csv_manager.generate_race_csv()
    
    root.mainloop()

if __name__ == "__main__":
    main()