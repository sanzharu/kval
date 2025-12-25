import tkinter as tk
from tkinter import ttk
from database import DatabaseManager, CSVLoader

class Application:
    def __init__(self, root):
        self.root = root
        self.db_manager = DatabaseManager()
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
        self.load(self.tree)
        
    def load(self, tree):
        db = self.db_manager.connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("""SELECT * FROM autovoksal.bus;""")
            
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
                
            self.db_manager.close_db()
            
    def sort(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("System")
        add_win.geometry("700x300")
        
        tree_frame = tk.Frame(add_win)
        tree_frame.pack()
        
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
            self.db_manager.close_db()
            
    def alpha(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("system")
        add_win.geometry("500x500")
        
        tree_frame = tk.Frame(add_win)
        tree_frame.pack()
        
        db = self.db_manager.connect_db()
        if db:
            cursor = db.cursor()
            cursor.execute("""select r.mark_bus, r.gos_number, sum(r.vmest) as total
    from bus r
    group by r.vmest, r.mark_bus, r.gos_number""")
            
            columns = ["Mark bus", "Gos number", "Total"]
            tree2 = ttk.Treeview(tree_frame, columns=columns, show="headings")
            for col in columns:
                tree2.heading(col, text=col)
                
            with open("alpha.txt", 'w') as f:
                f.write("\t".join(columns) + "\n")
                
                for row in cursor.fetchall():
                    tree2.insert("", "end", values=row)
                    f.write("\t".join(str(item) for item in row) + "\n")
                    
            tree2.pack()
            self.db_manager.close_db()

def main():
    root = tk.Tk()
    app = Application(root)
    
    # Загрузка данных из CSV файла (опционально)
    # db_manager = DatabaseManager()
    # csv_loader = CSVLoader(db_manager)
    # csv_loader.load_data_from_csv()
    
    root.mainloop()

if __name__ == "__main__":
    main()