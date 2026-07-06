# Project 4 – PDF Toolkit

A PDF utility project that supports common workflow tasks:

- Merge PDFs
- Split PDFs into single-page files
- Rotate PDF pages
- Extract PDF text to plain text files

## Files

- `main.py` - toolkit script
- `README.md` - documentation
- `output/` - generated PDF and text outputs
- `samples/` - sample PDFs to use with the toolkit

## Usage

1. Install dependencies:

```bash
pip install PyPDF2
```

2. Add sample PDFs to `samples/`.

3. Update `main.py` to call the desired function.

4. Run:

```bash
python main.py
```

## Functions

- `merge_pdfs(input_files, output_file)`
- `split_pdf(input_file, output_dir)`
- `rotate_pdf(input_file, output_file, rotation)`
- `extract_text(input_file, output_file)`
