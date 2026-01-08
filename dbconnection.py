import psycopg2

class DbConnection:
    
    def __init__(self, config):
        self.dbname = config.dbname
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.prefix = config.dbtableprefix
        
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            print("\nПроверьте:")
            print("1. Запущен ли PostgreSQL сервер")
            print("2. Правильность настроек в config.yaml")
            print("3. Существует ли база данных '{self.dbname}'")
            exit(1)
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
    
    def test_connection(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return True
        except:
            return False