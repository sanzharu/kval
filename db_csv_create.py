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

class CSVGenerator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
    def generate_csv_file(self, filename='data.csv'):
        try:
            # Данные для CSV файла
            bus_data = [
                ["bus_id", "mark_bus", "gos_number", "vmest"],
                ["1", "Mercedes Sprinter", "А123ВС77", "20"],
                ["2", "Ford Transit", "В456DE77", "15"],
                ["3", "Volkswagen Crafter", "С789FG77", "25"],
                ["4", "Peugeot Boxer", "Н321КЛ77", "18"],
                ["5", "Citroen Jumper", "Р753МН77", "22"],
                ["6", "Fiat Ducato", "Т159ОР77", "17"],
                ["7", "Renault Master", "У246СВ77", "24"],
                ["8", "Iveco Daily", "Х468НМ77", "19"]
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(bus_data)
            
            print(f"CSV file {filename} generated successfully")
            
        except Exception as e:
            print(f"Error generating CSV file: {e}")
            
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