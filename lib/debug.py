import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import CONN, CURSOR


def reset_tables():
    """(Optional) Clear all data for clean testing."""
    CURSOR.execute("DELETE FROM articles")
    CURSOR.execute("DELETE FROM magazines")
    CURSOR.execute("DELETE FROM authors")
    CONN.commit()

def seed_data():
    """Create sample data and test save methods."""
    # Authors
    a1 = Author("Alice Smith")
    a2 = Author("Bob Johnson")
    a3 = Author("Charlie Rose")
    a1.save()
    a2.save()
    a3.save()

    # Magazines
    m1 = Magazine("Tech Today", "Technology")
    m2 = Magazine("Healthy Living", "Health")
    m3 = Magazine("World Politics", "News")
    m1.save()
    m2.save()
    m3.save()

    # Articles
    Article("AI in 2025", a1.id, m1.id).save()
    Article("Mindful Eating", a1.id, m2.id).save()
    Article("Election 2024", a2.id, m3.id).save()
    Article("Tech Trends", a2.id, m1.id).save()
    Article("Mental Health Tips", a1.id, m2.id).save()
    Article("Policy Reform", a2.id, m3.id).save()
    Article("Gadget Reviews", a3.id, m1.id).save()
    Article("Quantum Computing", a1.id, m1.id).save()
    Article("VR Innovations", a1.id, m1.id).save()

def test_author_methods():
    print("\n=== Testing Author Methods ===")
    author = Author.find_by_name("Alice Smith")
    print(f"Author found: {author.name} (ID: {author.id})")

    print("\nArticles by Alice:")
    for art in author.articles():
        print(f"- {art.title}")

    print("\nMagazines Alice contributed to:")
    for mag in author.magazines():
        print(f"- {mag.name}")

    print("\nAdding article via add_article()...")
    author.add_article(Magazine.find_by_name("Tech Today"), "Future Chips")
    for art in author.articles():
        print(f"- {art.title}")

    print("\nTopic areas (categories) Alice has written in:")
    print(author.topic_areas())

    print("\nMost prolific author:")
    prolific = Author.most_prolific()
    print(f"- {prolific.name}")

def test_magazine_methods():
    print("\n=== Testing Magazine Methods ===")
    mag = Magazine.find_by_name("Tech Today")
    print(f"Magazine found: {mag.name} (ID: {mag.id})")

    print("\nArticles in magazine:")
    for art in mag.articles():
        print(f"- {art.title}")

    print("\nContributors to Tech Today:")
    for author in mag.contributors():
        print(f"- {author.name}")

    print("\nArticle titles in Tech Today:")
    print(mag.article_titles())

    print("\nContributing authors (more than 2 articles):")
    for author in mag.contributing_authors():
        print(f"- {author.name}")

    print("\nTop publisher magazine:")
    top_mag = Magazine.top_publisher()
    if top_mag:
        articles_count = len(top_mag.articles())
        print(f"- {top_mag.name} (Articles: {articles_count})")
    else:
        print("No magazines with articles found.")

def test_class_lookup():
    print("\n=== Testing Class Lookup Methods ===")
    found = Author.find_by_id(1)
    print(f"Author with ID 1: {found.name if found else 'Not found'}")

    found = Magazine.find_by_id(1)
    print(f"Magazine with ID 1: {found.name if found else 'Not found'}")

    found = Article.find_by_id(1)
    print(f"Article with ID 1: {found.title if found else 'Not found'}")

    found = Article.find_by_title("Tech Trends")
    print(f"Article by title: {found.title} by Author ID {found.author_id}")

def test_relationship_methods():
    print("\n=== Testing Relationship Methods ===")
    article = Article.find_by_title("Tech Trends")
    print(f"Author of '{article.title}': {article.author().name}")
    print(f"Magazine of '{article.title}': {article.magazine().name}")

def run_all():
    print("Resetting tables...")
    reset_tables()

    print("Seeding data...")
    seed_data()

    test_author_methods()
    test_magazine_methods()
    test_class_lookup()
    test_relationship_methods()

if __name__ == "__main__":
    run_all()
