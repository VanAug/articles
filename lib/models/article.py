
from lib.db.connection import CONN, CURSOR

class Article:

    def __init__(self, title, author_id, magazine_id, id = None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if isinstance(title, str) and 1 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Title must be a non empty string less than 50")
        
    def save(self):
        if self.id:
            CURSOR.execute("UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?", (self.title, self.author_id, self.magazine_id, self.id))
        else:
            CURSOR.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (self.title, self.author_id, self.magazine_id))
            self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM articles WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) if row else None
    
    @classmethod
    def find_by_title(cls, title):
        sql = """
            SELECT * FROM articles WHERE title = ?
        """
        CURSOR.execute(sql, (title,))
        row = CURSOR.fetchone()
        return cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) if row else None
    
    @classmethod
    def find_by_author(cls, author_id):
        sql = """
            SELECT * FROM articles WHERE author_id = ?
        """
        CURSOR.execute(sql, (author_id,))
        rows = CURSOR.fetchall()
        return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]
       
    @classmethod
    def find_by_magazine(cls, magazine_id):
        sql = """
            SELECT * FROM articles WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (magazine_id,))
        rows = CURSOR.fetchall()
        return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]
    
    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)