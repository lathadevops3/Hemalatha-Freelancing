import sqlite3
from pathlib import Path
import pandas as pd

DB_FILE = Path(__file__).parent / "employees.db"


def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            title TEXT,
            salary REAL,
            hire_date TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_employee(name, department, title, salary, hire_date):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, department, title, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
        (name, department, title, salary, hire_date),
    )
    conn.commit()
    conn.close()
    print(f"Added employee: {name}")


def update_employee(employee_id, **fields):
    if not fields:
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    columns = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values()) + [employee_id]
    cursor.execute(f"UPDATE employees SET {columns} WHERE id = ?", values)
    conn.commit()
    conn.close()
    print(f"Updated employee ID {employee_id}")


def delete_employee(employee_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    conn.close()
    print(f"Deleted employee ID {employee_id}")


def list_employees():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    print(df)
    return df


def search_employees(query):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT * FROM employees WHERE name LIKE ? OR department LIKE ? OR title LIKE ?",
        conn,
        params=(f"%{query}%", f"%{query}%", f"%{query}%"),
    )
    conn.close()
    print(df)
    return df


def export_to_excel(output_file):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    df.to_excel(output_file, index=False)
    print(f"Exported employee report to {output_file}")


def department_summary():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT department, COUNT(*) AS count, AVG(salary) AS avg_salary FROM employees GROUP BY department", conn)
    conn.close()
    print(df)
    return df


def main():
    initialize_db()
    print("Employee Management System")
    if not DB_FILE.exists() or list_employees().empty:
        add_employee("Aisha Khan", "Engineering", "Software Engineer", 70000, "2024-03-01")
        add_employee("Ravi Patel", "Sales", "Account Executive", 62000, "2023-11-15")
        add_employee("Mina George", "HR", "HR Manager", 65000, "2024-01-20")
        add_employee("Jules Kim", "Engineering", "DevOps Engineer", 80000, "2024-04-10")

    list_employees()
    search_employees("Engineering")
    update_employee(1, title="Senior Software Engineer", salary=80000)
    delete_employee(2)
    department_summary()
    export_to_excel(Path(__file__).parent / "employee_report.xlsx")


if __name__ == "__main__":
    main()
