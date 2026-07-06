from pathlib import Path
from typing import List

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
SAMPLES_DIR = BASE_DIR / "samples"
OUTPUT_DIR.mkdir(exist_ok=True)
SAMPLES_DIR.mkdir(exist_ok=True)


def merge_pdfs(input_files: List[Path], output_file: Path) -> None:
    writer = PdfWriter()
    for pdf_path in input_files:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_file, "wb") as out_file:
        writer.write(out_file)
    print(f"Merged {len(input_files)} files into {output_file}")


def split_pdf(input_file: Path, output_dir: Path) -> None:
    reader = PdfReader(input_file)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = output_dir / f"{input_file.stem}_page_{i}.pdf"
        with open(out_path, "wb") as out_file:
            writer.write(out_file)
    print(f"Split {input_file.name} into {len(reader.pages)} pages")


def rotate_pdf(input_file: Path, output_file: Path, rotation: int) -> None:
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(rotation)
        writer.add_page(page)
    with open(output_file, "wb") as out_file:
        writer.write(out_file)
    print(f"Rotated {input_file.name} by {rotation} degrees to {output_file}")


def extract_text(input_file: Path, output_file: Path) -> None:
    reader = PdfReader(input_file)
    lines = []
    for page in reader.pages:
        lines.append(page.extract_text() or "")
    output_file.write_text("\n\n".join(lines), encoding="utf-8")
    print(f"Extracted text from {input_file.name} to {output_file}")


def create_sample_pdfs() -> List[Path]:
    SAMPLES_DIR.mkdir(exist_ok=True)
    samples = [
        SAMPLES_DIR / "sample1.pdf",
        SAMPLES_DIR / "sample2.pdf",
    ]

    for index, sample_path in enumerate(samples, start=1):
        if sample_path.exists():
            continue
        c = canvas.Canvas(str(sample_path), pagesize=letter)
        for page_number in range(1, 3):
            c.setFont("Helvetica", 14)
            c.drawString(72, 720, f"Sample PDF {index} - Page {page_number}")
            c.drawString(72, 700, "This is a demonstration PDF with visible text.")
            c.drawString(72, 680, "Use this file to test merge, split, rotate, and extract functionalities.")
            c.showPage()
        c.save()
        print(f"Created sample PDF: {sample_path.name}")

    return samples


def demo() -> None:
    print("PDF Toolkit Demo")
    sample_files = create_sample_pdfs()

    merged_pdf = OUTPUT_DIR / "merged.pdf"
    merge_pdfs(sample_files, merged_pdf)

    split_pdf(merged_pdf, OUTPUT_DIR)

    rotated_pdf = OUTPUT_DIR / "rotated_sample1.pdf"
    rotate_pdf(sample_files[0], rotated_pdf, 90)

    extracted_text = OUTPUT_DIR / "sample1_text.txt"
    extract_text(sample_files[0], extracted_text)

    print("Demo complete. Check the output/ directory.")


if __name__ == "__main__":
    demo()
