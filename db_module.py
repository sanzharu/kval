import pymysql


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