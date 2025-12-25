import csv

class CSVManager:
    def __init__(self):
        pass
        
    def generate_bus_csv(self, filename='bus_data.csv'):
        try:
            # Данные для CSV файла с автобусами
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
            return filename
            
        except Exception as e:
            print(f"Error generating CSV file: {e}")
            return None
            
    def generate_race_csv(self, filename='race_data.csv'):
        try:
            # Данные для CSV файла с рейсами
            race_data = [
                ["race_id", "bus_id", "station_id", "passenger_count"],
                ["1", "1", "101", "18"],
                ["2", "2", "102", "14"],
                ["3", "3", "101", "22"],
                ["4", "1", "103", "19"],
                ["5", "4", "102", "17"],
                ["6", "5", "101", "20"],
                ["7", "3", "103", "23"],
                ["8", "2", "101", "13"]
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(race_data)
            
            print(f"CSV file {filename} generated successfully")
            return filename
            
        except Exception as e:
            print(f"Error generating CSV file: {e}")
            return None