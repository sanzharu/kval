import pymysql
import csv

class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='root', database='autovoksal'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect_db(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Successful db connection")
            return self.connection
        except Exception as e:
            print(f"NOT {e}")
            return None
            
    def close_db(self):
        if self.connection:
            self.connection.close()

class CSVLoader:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def load_data_from_csv(self, filename='data.csv'):
        db = self.db_manager.connect_db()
        if not db:
            return
            
        try:
            cursor = db.cursor()
            
            with open(filename, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Пропускаем заголовок
                
                for row in csv_reader:
                    if len(row) >= 4:
                        query = """
                        INSERT INTO bus (bus_id, mark_bus, gos_number, vmest) 
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        mark_bus = VALUES(mark_bus),
                        gos_number = VALUES(gos_number),
                        vmest = VALUES(vmest)
                        """
                        cursor.execute(query, (row[0], row[1], row[2], row[3]))
                        
            db.commit()
            print(f"Data from {filename} successfully loaded to database")
            
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            db.rollback()
            
        finally:
            self.db_manager.close_db()