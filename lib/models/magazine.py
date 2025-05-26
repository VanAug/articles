
from lib.db.connection import CONN, CURSOR

class Magazine:
    
    def __init__(self, name, category, id = None):
        self.id = id
        self.name = name
        self.category = category

        @property
        def name(self):
            return self._name
    
        @name.setter
        def name(self, name):
            if isinstance(name, str) and 1 <= len(name) <= 25:
                self._name = name
            else:
                raise ValueError("Magazine name must be a non empty string less tan 25 charactres.")
            
        @property
        def category(self):
            return self._category

        @category.setter
        def category(self, category):
            if isinstance(category, str):
                self._category = category
            else:
                raise ValueError("Category must be a string")
            
        def save(self):
            if self.id:
                CURSOR.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
            else:
                CURSOR.execute("INSERT INTO magazines (name, category), VALUES (?, ?)", (self.name, self.category))
                self.id = CURSOR.lastrowid
            CONN.commit()

        @classmethod
        def find_by_id(cls, id):
            sql = """
                SELECT * FROM magazines WHERE id = ?
            """
            CURSOR.execute(sql, (id,))
            row = CURSOR.fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        
        @classmethod
        def find_by_name(cls, name):
            sql = """
                SELECT * FROM magazines WHERE name = ?
            """
            CURSOR.execute(sql, (name,))
            row = CURSOR.fetchone()
            return cls(row["name"], row["category"], row["id"]) if row else None
        
        @classmethod
        def find_by_category(cls, category):
            sql = """
                SELECT * FROM magazines WHERE category = ?
            """
            CURSOR.execute(sql, (category,))
            rows = CURSOR.fetchall()
            return [cls(row["name"], row["category"], row["id"]) for row in rows]
        
        def articles(self):
            pass


