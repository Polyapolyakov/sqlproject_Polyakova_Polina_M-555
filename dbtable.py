from dbconnection import *

class DbTable:
    
    dbconn = None
    
    def table_name(self):
        return self.dbconn.prefix + "table"
    
    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"]}
    
    def primary_key(self):
        return ['id']
    
    def column_names_without_id(self):
        res = list(self.columns().keys())
        if 'id' in res:
            res.remove('id')
        return sorted(res)
    
    def table_constraints(self):
        return []
    
    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in sorted(self.columns().items())]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
    
    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name() + " CASCADE"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
    
    def insert_one(self, vals):
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        placeholders = ", ".join(["%s"] * len(vals))
        sql += placeholders + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
    
    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        if 'name' in self.columns():
            sql += " ORDER BY name"
        else:
            sql += " ORDER BY "
            sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    
    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        if 'name' in self.columns():
            sql += " ORDER BY name"
        else:
            sql += " ORDER BY "
            sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (num - 1,))
        return cur.fetchone()