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
                ADD COLUMN IF NOT EXISTS product_key TEXT,
                ADD COLUMN IF NOT EXISTS name TEXT,
                ADD COLUMN IF NOT EXISTS unit TEXT DEFAULT 'pezzo',
                ADD COLUMN IF NOT EXISTS default_quantity NUMERIC(10,3) NOT NULL DEFAULT 1.0,
                ADD COLUMN IF NOT EXISTS allow_fractional_quantity BOOLEAN NOT NULL DEFAULT FALSE,
                ADD COLUMN IF NOT EXISTS canonical_unit TEXT;

            UPDATE products
            SET
                name = COALESCE(name, canonical_name),
                unit = COALESCE(unit, quantity_unit, 'pezzo'),
                default_quantity = COALESCE(default_quantity, quantity_value, 1.0),
                canonical_unit = COALESCE(
                    canonical_unit,
                    CASE
                        WHEN LOWER(COALESCE(unit, quantity_unit, '')) IN
                             ('kg','kilogram','kilograms') THEN 'kg'
                        WHEN LOWER(COALESCE(unit, quantity_unit, '')) IN
                             ('l','litro','liter','liters') THEN 'l'
                        WHEN LOWER(COALESCE(unit, quantity_unit, '')) IN
                             ('confezione','package','pack') THEN 'pack'
                        WHEN LOWER(COALESCE(unit, quantity_unit, '')) IN
                             ('pezzo','piece') THEN 'piece'
                        ELSE LOWER(COALESCE(unit, quantity_unit, 'pezzo'))
                    END
                );

            UPDATE products
            SET allow_fractional_quantity = TRUE
            WHERE canonical_unit IN ('kg', 'l');

            CREATE UNIQUE INDEX IF NOT EXISTS idx_products_product_key
            ON products(product_key)
            WHERE product_key IS NOT NULL;

            CREATE INDEX IF NOT EXISTS idx_products_product_key_unit
            ON products(product_key, canonical_unit);
        """)

    conn.commit()

print("Database inizializzato correttamente.")
