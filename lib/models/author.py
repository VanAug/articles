
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

    #Add instance to table   
    def save(self):
        if self.id:
            CURSOR.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        else:
            CURSOR.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = CURSOR.lastrowid
        CONN.commit()

    #find author by id
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM authors WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls(row["name"], row["id"]) if row else None
    
    #find author by name
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM authors WHERE name = ?
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls(row["name"], row["id"]) if row else None
    
    #Find author with most articles    
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
    
    #find all articles by author id
    def articles(self):
        from lib.models.article import Article
        return Article.find_by_author(self.id)

    #find magazines contributed to by author.
    def magazines(self):
        from lib.models.magazine import Magazine
        articles = self.articles()
        magazine_ids = {article.magazine_id for article in articles}
        return [Magazine.find_by_id(mag_ids) for mag_ids in magazine_ids]

    #Add new article by author 
    def add_article(self, magazine, title):
        from lib.models.article import Article
        if not self.id or not magazine.id:
            raise ValueError("Both author and magazine must be instances before adding article")
        article = Article(title, self.id, magazine.id)
        article.save()
        return article
    
    #Show topic areas by author
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
