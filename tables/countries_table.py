from dbtable import *

class CountriesTable(DbTable):
    
    def table_name(self):
        return self.dbconn.prefix + "countries"
    
    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "name": ["varchar(255)", "NOT NULL", "UNIQUE"]
        }
    
    def find_by_name(self, name):
        sql = "SELECT * FROM " + self.table_name() + " WHERE LOWER(name) = LOWER(%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (name.strip(),))
        return cur.fetchone()
    
    def delete_by_name(self, name):
        country = self.find_by_name(name)
        if not country:
            return 0
        
        sql = "DELETE FROM " + self.table_name() + " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (country[0],))
        self.dbconn.conn.commit()
        return cur.rowcount
    
    def update_by_name(self, old_name, new_name):
        sql = "UPDATE " + self.table_name() + " SET name = %s WHERE LOWER(name) = LOWER(%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (new_name.strip(), old_name.strip()))
        self.dbconn.conn.commit()
        return cur.rowcount
    
    def check_name_exists(self, name):
        sql = "SELECT COUNT(*) FROM " + self.table_name() + " WHERE LOWER(name) = LOWER(%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (name.strip(),))
        result = cur.fetchone()
        return result[0] > 0
    
    def get_country_movies_count(self, name):
        country = self.find_by_name(name)
        if not country:
            return 0
        
        sql = """
        SELECT COUNT(*) FROM """ + self.dbconn.prefix + """movies m
        JOIN """ + self.table_name() + """ c ON m.country_id = c.id
        WHERE c.name = %s
        """
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (name,))
        result = cur.fetchone()
        return result[0]