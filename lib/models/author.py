
from lib.db.connection import CONN, CURSOR
class Author:

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
        return cls(row["name"], row["id"]) if row else None
    
    @classmethod
    def most_articles(cls):
        CURSOR.execute("""
            SELECT author_id, COUNT(*) as count FROM articles
            GROUP BY author_id
            ORDER BY count DESC
            LIMIT 1
        """)
        row = CURSOR.fetchone()
        return cls.find_by_id(row["author_id"]) if row else None
    
    @classmethod
    def most_prolific(cls):
        sql = """
            SELECT a.*, COUNT(art.id) as article_count
            FROM authors a
            JOIN articles art ON a.id = art.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1 
        """
        CURSOR.execute(sql)
        row = CURSOR.fetchone()
        return cls(row["name"], row["id"]) if row else None
    
    def articles(self):
        from lib.models.article import Article
        return Article.find_by_author(self.id)

    def magazines(self):
        articles = self.articles()
        return list({article.magazine() for article in articles})

    def add_article(self, magazine, title):
        from lib.models.article import Article
        if not self.id or not magazine.id:
            raise ValueError("Both author and magazine must be instances before adding article")
        article = Article(title, self.id, magazine.id)
        article.save()
        return article
    
    def topic_areas(self):
        sql = """
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [row["category"] for row in rows]
