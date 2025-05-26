
from lib.db.connection import CONN, CURSOR
class Authors:

    def __init__(self, name, id = None):
        self.id = id
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and 1 <= len(name) <= 25:
            self._name = name
        else:
            raise ValueError("Author name must be a non empty string less tan 25 charactres.")
        
    def save(self):
        if self.id:
            CURSOR.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        else:
            CURSOR.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM authors WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls(row["name"], row["id"]) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM authors WHERE name = ?
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls(row["name"], row["name"]) if row else None
    
    def articles(self):
        pass

    def magazines(self):
        pass
    
