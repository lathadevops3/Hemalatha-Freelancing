from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "inputs"
OUTPUT_FILE = BASE_DIR / "output.xlsx"
EXPECTED_COLUMNS = {"Name", "Sales", "Region", "Date", "Product"}


def find_input_files(input_dir: Path):
    files = sorted(input_dir.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No .xlsx files found in {input_dir}")
    return files


def load_sales_data(paths):
    frames = []
    for path in paths:
        print(f"Loading file: {path.name}")
        df = pd.read_excel(path)
        if not EXPECTED_COLUMNS.issubset(df.columns):
            missing = EXPECTED_COLUMNS - set(df.columns)
            raise ValueError(f"{path.name} missing columns: {missing}")
        df["Date"] = pd.to_datetime(df["Date"])
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def summarize_sales(df):
    total_sales = int(df["Sales"].sum())
    average_sales = float(df["Sales"].mean())
    highest = df.loc[df["Sales"].idxmax()]
    lowest = df.loc[df["Sales"].idxmin()]
    sales_by_region = df.groupby("Region")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
    sales_by_product = df.groupby("Product")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
    monthly_total = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    monthly_total["Date"] = monthly_total["Date"].dt.to_timestamp()

    return {
        "total": total_sales,
        "average": average_sales,
        "highest_name": str(highest["Name"]),
        "highest_value": int(highest["Sales"]),
        "highest_row": highest.to_dict(),
        "lowest_name": str(lowest["Name"]),
        "lowest_value": int(lowest["Sales"]),
        "sales_by_region": sales_by_region,
        "sales_by_product": sales_by_product,
        "monthly_total": monthly_total,
        "table": df,
    }


def print_summary(summary):
    print(f"Total Sales: {summary['total']}")
    print(f"Average Sales: {summary['average']:.2f}")
    print(f"Highest Sale: {summary['highest_name']} ({summary['highest_value']})")
    print(f"Lowest Sale: {summary['lowest_name']} ({summary['lowest_value']})")
    print("\nSales by Region:")
    print(summary["sales_by_region"].to_string(index=False))
    print("\nSales by Product:")
    print(summary["sales_by_product"].to_string(index=False))
    print("\nMonthly Sales Totals:")
    print(summary["monthly_total"].to_string(index=False))


def save_summary(path: Path, summary):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        summary["table"].to_excel(writer, sheet_name="All Sales", index=False)
        summary["sales_by_region"].to_excel(writer, sheet_name="Sales by Region", index=False)
        summary["sales_by_product"].to_excel(writer, sheet_name="Sales by Product", index=False)
        summary["monthly_total"].to_excel(writer, sheet_name="Monthly Sales", index=False)

        metrics = pd.DataFrame(
            [
                {"Metric": "Total Sales", "Value": summary["total"]},
                {"Metric": "Average Sales", "Value": summary["average"]},
                {
                    "Metric": "Highest Sale",
                    "Value": f"{summary['highest_name']} ({summary['highest_value']})",
                },
                {
                    "Metric": "Lowest Sale",
                    "Value": f"{summary['lowest_name']} ({summary['lowest_value']})",
                },
            ]
        )
        metrics.to_excel(writer, sheet_name="Summary", index=False)


def main():
    print("Real-Time Excel Sales Report Generator")
    input_files = find_input_files(INPUT_DIR)
    sales_df = load_sales_data(input_files)
    report = summarize_sales(sales_df)
    print_summary(report)
    save_summary(OUTPUT_FILE, report)
    print(f"Saved summary report to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
