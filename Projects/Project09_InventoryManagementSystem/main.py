import sqlite3
from pathlib import Path
import pandas as pd

DB_FILE = Path(__file__).parent / "inventory.db"
OUTPUT_FILE = Path(__file__).parent / "inventory_report.xlsx"


def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sku TEXT,
            quantity INTEGER,
            reorder_level INTEGER,
            price REAL
        )
        """
    )
    conn.commit()
    conn.close()


def add_product(name, sku, quantity, reorder_level, price):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, sku, quantity, reorder_level, price) VALUES (?, ?, ?, ?, ?)",
        (name, sku, quantity, reorder_level, price),
    )
    conn.commit()
    conn.close()
    print(f"Added product: {name}")


def update_stock(sku, quantity):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE sku = ?", (quantity, sku))
    conn.commit()
    conn.close()
    print(f"Updated stock for SKU: {sku}")


def delete_product(sku):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE sku = ?", (sku,))
    conn.commit()
    conn.close()
    print(f"Deleted product SKU: {sku}")


def list_products():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    print(df)
    return df


def low_stock_alerts():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM products WHERE quantity <= reorder_level", conn)
    conn.close()
    print("Low stock products:")
    print(df)
    return df


def inventory_report():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT name, sku, quantity, reorder_level, price, quantity * price AS inventory_value FROM products",
        conn,
    )
    conn.close()
    print("Inventory report:")
    print(df)
    return df


def export_to_excel(output_file):
    df = inventory_report()
    df.to_excel(output_file, index=False)
    print(f"Exported inventory report to {output_file}")


def main():
    initialize_db()
    print("Inventory Management System")
    if not DB_FILE.exists() or list_products().empty:
        add_product("Wireless Mouse", "WM-001", 25, 10, 19.99)
        add_product("Keyboard", "KB-002", 12, 5, 29.99)
        add_product("Webcam", "WC-003", 4, 5, 49.99)

    update_stock("WC-003", 8)
    delete_product("KB-002")
    list_products()
    low_stock_alerts()
    export_to_excel(OUTPUT_FILE)


if __name__ == "__main__":
    main()
