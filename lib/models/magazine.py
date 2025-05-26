
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
            CURSOR.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
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
    
    @classmethod
    def magazine_with_multiple_authors(cls):
        sql = """
            SELECT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) >= 2
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls(row["name"], row["category"], row["id"]) for row in rows]

    @classmethod
    def article_count(cls):
        sql = """
            SELECT m.name, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """
        CURSOR.execute(sql)
        return CURSOR.fetchall()

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_magazine(self.id)
    
    def authors(self):
        from lib.models.article import Article
        from lib.models.author import Author
        articles = Article.find_by_magazine(self.id)
        return list ({article.author() for article in articles})
    
    def contributors(self):
        from lib.models.author import Author
        sql = """
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row["name"], row["id"]) for row in rows]
    
    def article_titles(self):
        sql = """
            SELECT title FROM articles WHERE magazine_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author
        sql = """
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row["name"], row["id"]) for row in rows]





