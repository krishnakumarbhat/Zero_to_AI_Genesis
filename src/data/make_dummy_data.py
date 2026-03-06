import json
import random
import sqlite3
from pathlib import Path

from faker import Faker


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
fake = Faker()
random.seed(7)


HR_TOPICS = [
    "paid time off",
    "remote work",
    "parental leave",
    "health insurance",
    "expense reimbursement",
    "code of conduct",
    "travel policy",
    "equipment stipend",
    "on-call compensation",
    "performance reviews",
]


def make_hr_faq(path: Path, n: int = 50) -> None:
    rows = []
    for i in range(n):
        topic = random.choice(HR_TOPICS)
        q = f"FAQ {i+1}: What is the company policy on {topic}?"
        a = (
            f"For {topic}, employees should submit requests through the HR portal. "
            f"Approval typically takes 2-5 business days. "
            f"Escalations go to hr-ops@fictionaltech.example."
        )
        rows.append({"id": i + 1, "question": q, "answer": a, "topic": topic})

    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_wiki_like_articles(path: Path) -> None:
    docs = [
        {
            "id": "hist-1",
            "title": "History of Printing",
            "text": "Johannes Gutenberg's printing press transformed information access in 15th-century Europe. Movable type lowered costs, accelerated literacy, and enabled scientific exchange.",
            "domain": "history",
        },
        {
            "id": "phys-1",
            "title": "Classical Mechanics",
            "text": "Classical mechanics models motion using force, mass, and acceleration. Newton's laws remain foundational for engineering and many everyday-scale systems.",
            "domain": "physics",
        },
        {
            "id": "mov-1",
            "title": "Film Editing",
            "text": "Film editing constructs narrative rhythm through shot selection and transitions. Continuity editing preserves spatial logic, while montage can create conceptual meaning.",
            "domain": "movies",
        },
    ]

    with path.open("w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def make_sqlite_db(path: Path, n_users: int = 100, n_products: int = 30, n_orders: int = 100) -> None:
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("DROP TABLE IF EXISTS Products")
    cur.execute("DROP TABLE IF EXISTS Orders")

    cur.execute(
        """
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            city TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE Products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            category TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE Orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(product_id) REFERENCES Products(id)
        )
        """
    )

    users = [(i + 1, fake.name(), fake.email(), fake.city()) for i in range(n_users)]
    cur.executemany("INSERT INTO Users VALUES (?, ?, ?, ?)", users)

    categories = ["Laptop", "Accessory", "Monitor", "Audio"]
    products = []
    for i in range(n_products):
        products.append(
            (
                i + 1,
                f"Product-{i+1}",
                round(random.uniform(19, 1999), 2),
                random.choice(categories),
            )
        )
    cur.executemany("INSERT INTO Products VALUES (?, ?, ?, ?)", products)

    orders = []
    for i in range(n_orders):
        orders.append(
            (
                i + 1,
                random.randint(1, n_users),
                random.randint(1, n_products),
                random.randint(1, 5),
                fake.iso8601(),
            )
        )
    cur.executemany("INSERT INTO Orders VALUES (?, ?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    make_hr_faq(DATA_DIR / "hr_faq.jsonl")
    make_wiki_like_articles(DATA_DIR / "wiki_like_articles.jsonl")
    make_sqlite_db(DATA_DIR / "company_store.db")
    print("Dummy data created in ./data")


if __name__ == "__main__":
    main()
