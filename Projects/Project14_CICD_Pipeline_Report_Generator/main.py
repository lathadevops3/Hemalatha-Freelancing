from pathlib import Path
import json
import pandas as pd


def create_sample_data(path: Path):
    sample = [
        {"id": 1, "pipeline": "build-and-test", "status": "success", "duration_seconds": 120},
        {"id": 2, "pipeline": "build-and-test", "status": "failure", "duration_seconds": 180},
        {"id": 3, "pipeline": "deploy", "status": "success", "duration_seconds": 90},
    ]
    path.write_text(json.dumps(sample, indent=2), encoding="utf-8")
    return path


def generate_report(json_path: Path, output_xlsx: Path):
    data = json.loads(json_path.read_text(encoding="utf-8"))
    df = pd.DataFrame(data)
    summary = df.groupby(["pipeline", "status"]).size().reset_index(name="count")
    metrics = df.groupby("pipeline")["duration_seconds"].agg(["mean", "max", "min"]).reset_index()

    with pd.ExcelWriter(output_xlsx, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="runs", index=False)
        summary.to_excel(writer, sheet_name="summary", index=False)
        metrics.to_excel(writer, sheet_name="metrics", index=False)

    print(f"Report written to {output_xlsx}")


def demo():
    base = Path(__file__).parent
    sample = base / "sample_ci_runs.json"
    create_sample_data(sample)
    out = base / "cicd_report.xlsx"
    generate_report(sample, out)


if __name__ == "__main__":
    demo()
