import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = Path(__file__).parent / "expenses.db"
OUTPUT_DIR = Path(__file__).parent


def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_expense(date, category, amount, description):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
        (date, category, amount, description),
    )
    conn.commit()
    conn.close()
    print(f"Added expense: {category} {amount}")


def update_expense(expense_id, **fields):
    if not fields:
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    columns = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values()) + [expense_id]
    cursor.execute(f"UPDATE expenses SET {columns} WHERE id = ?", values)
    conn.commit()
    conn.close()
    print(f"Updated expense ID {expense_id}")


def delete_expense(expense_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    print(f"Deleted expense ID {expense_id}")


def list_expenses():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    print(df)
    return df


def monthly_report(month):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ?", conn, params=(month,)
    )
    conn.close()
    print(df)
    return df


def category_summary():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category", conn
    )
    conn.close()
    print(df)
    return df


def export_to_excel(output_file):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    df.to_excel(output_file, index=False)
    print(f"Exported expenses to {output_file}")


def save_category_chart(df, output_file):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df["category"], df["total"], color="#4c72b0")
    ax.set_title("Expenses by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Amount")
    fig.tight_layout()
    fig.savefig(output_file)
    plt.close(fig)
    print(f"Saved category chart to {output_file}")


def main():
    initialize_db()
    print("Expense Tracker")
    if not DB_FILE.exists() or list_expenses().empty:
        add_expense("2024-06-05", "Office", 120.50, "Printer ink")
        add_expense("2024-06-08", "Food", 45.00, "Team lunch")
        add_expense("2024-07-01", "Travel", 310.75, "Client site visit")
        add_expense("2024-07-12", "Subscriptions", 99.99, "SaaS tools")

    list_expenses()
    monthly_report("2024-06")
    update_expense(1, amount=125.75)
    delete_expense(2)
    category_summary()
    export_to_excel(OUTPUT_DIR / "expense_report.xlsx")
    save_category_chart(category_summary(), OUTPUT_DIR / "expense_category_chart.png")


if __name__ == "__main__":
    main()
