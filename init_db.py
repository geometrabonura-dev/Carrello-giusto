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

        # Adegua la tabella products alle colonne richieste dal backend
        cur.execute("""
            ALTER TABLE products
            ADD COLUMN IF NOT EXISTS product_key TEXT,
            ADD COLUMN IF NOT EXISTS name TEXT,
            ADD COLUMN IF NOT EXISTS unit TEXT DEFAULT 'pezzo',
            ADD COLUMN IF NOT EXISTS default_quantity DOUBLE PRECISION DEFAULT 1.0;
        """)

    conn.commit()

print("Database inizializzato correttamente.")
