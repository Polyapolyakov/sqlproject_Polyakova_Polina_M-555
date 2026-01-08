from dbtable import *

class MoviesTable(DbTable):
    
    def table_name(self):
        return self.dbconn.prefix + "movies"
    
    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "title": ["varchar(255)", "NOT NULL"],
            "year_release": ["integer", "NOT NULL", "CHECK (year_release > 0)"],
            "country_id": ["integer", "NOT NULL", "REFERENCES countries(id) ON DELETE CASCADE"],
            "duration": ["integer", "NOT NULL", "CHECK (duration > 0)"],
            "min_age": ["integer", "NOT NULL", "CHECK (min_age >= 0)"]
        }
    
    def find_by_position_and_country(self, num, country_name):
        sql = """
        SELECT m.* FROM """ + self.table_name() + """ m
        JOIN """ + self.dbconn.prefix + """countries c ON m.country_id = c.id
        WHERE c.name = %s
        ORDER BY m.title
        LIMIT 1 OFFSET %s
        """
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (country_name, num - 1))
        return cur.fetchone()
    
    def all_by_country_name(self, country_name):
        sql = """
        SELECT m.*, c.name as country_name FROM """ + self.table_name() + """ m
        JOIN """ + self.dbconn.prefix + """countries c ON m.country_id = c.id
        WHERE c.name = %s
        ORDER BY m.title
        """
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (country_name,))
        return cur.fetchall()
    
    def delete_by_position_and_country(self, num, country_name):
        movie = self.find_by_position_and_country(num, country_name)
        if not movie:
            return 0
        
        sql = "DELETE FROM " + self.table_name() + " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (movie[0],))
        self.dbconn.conn.commit()
        return cur.rowcount
    
    def insert_for_country(self, title, year, country_name, duration, min_age):
        sql = "SELECT id FROM " + self.dbconn.prefix + "countries WHERE name = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (country_name,))
        country = cur.fetchone()
        
        if not country:
            raise Exception(f"Страна '{country_name}' не найдена!")
        
        if year <= 0:
            raise Exception("Год выпуска должен быть положительным числом!")
        if duration <= 0:
            raise Exception("Продолжительность должна быть положительным числом!")
        if min_age < 0:
            raise Exception("Минимальный возраст не может быть отрицательным!")
        
        self.insert_one([title, year, country[0], duration, min_age])