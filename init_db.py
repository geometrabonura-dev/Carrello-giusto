import os
from pathlib import Path
import psycopg

database_url = os.environ["DATABASE_URL"]
schema_file = Path("/app/sql/schema.sql")

print("Inizializzazione database CarrelloGiusto...")

sql = schema_file.read_text(encoding="utf-8")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute(sql)

        cur.execute("""
            ALTER TABLE products
            ADD COLUMN IF NOT EXISTS product_key TEXT;
        """)

        cur.execute("""
            UPDATE products
            SET product_key = id::text
            WHERE product_key IS NULL;
        """)

    conn.commit()

print("Database inizializzato correttamente.")
