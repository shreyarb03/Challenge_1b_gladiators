"""import fitz  # PyMuPDF
import csv
from pathlib import Path

# --- Configuration ---
PDF_DIR = Path("/Collection/pdfs")
OUTPUT_CSV = "output_chunks.csv"
HEADING_HINTS = {"instructions:", "ingredients:"}

# --- Utility ---
def extract_lines_from_page(page):
    blocks = page.get_text("dict")["blocks"]
    lines = []
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            # Remove bullet points like "•"
            non_bullet_spans = [
                span["text"].strip()
                for span in line["spans"]
                if span["text"].strip() != "•"
            ]
            text = " ".join(non_bullet_spans).strip()
            if not text:
                continue
            span = line["spans"][0]
            font_size = round(span["size"], 2)
            bold = "Bold" in span["font"]
            lines.append({
                "text": text,
                "font_size": font_size,
                "bold": bold
            })
    return lines

def is_heading(text, font_size, bold):
    stripped = text.strip().lower()
    if stripped in HEADING_HINTS:
        return True
    if text.endswith(":") and len(text) < 40:
        return True
    if bold or font_size >= 14:
        return True
    return False

# --- Main Extraction ---
def extract_chunks():
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout)
        writer.writerow(["type", "text", "font_size", "bold", "page", "document"])

        for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
            doc = fitz.open(pdf_path)
            print(f"📄 Processing {pdf_path.name} ...")

            for page_number, page in enumerate(doc):
                lines = extract_lines_from_page(page)
                previous_was_heading = False

                for line in lines:
                    text = line["text"]
                    font_size = line["font_size"]
                    bold = line["bold"]

                    is_head = is_heading(text, font_size, bold)

                    # Downgrade consecutive headings
                    if is_head:
                        if previous_was_heading:
                            line_type = "BODY"
                        else:
                            line_type = "HEADING"
                            previous_was_heading = True
                    else:
                        line_type = "BODY"
                        previous_was_heading = False

                    writer.writerow([
                        line_type, text, font_size, bold, page_number + 1, pdf_path.name
                    ])
            doc.close()

    print(f"\n Extraction completed. Output saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    extract_chunks()"""

import fitz  # PyMuPDF
import csv
from pathlib import Path

# --- Configuration ---
PDF_DIR = Path("/Collection/pdfs")
OUTPUT_CSV = "output_chunks.csv"
HEADING_HINTS = {"instructions:", "ingredients:"}

# --- Utility ---
def extract_lines_from_page(page):
    blocks = page.get_text("dict")["blocks"]
    lines = []
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            # Remove bullet points like "•"
            non_bullet_spans = [
                span["text"].strip()
                for span in line["spans"]
                if span["text"].strip() != "•"
            ]
            text = " ".join(non_bullet_spans).strip()
            if not text:
                continue
            span = line["spans"][0]
            font_size = round(span["size"], 2)
            bold = "Bold" in span["font"]
            lines.append({
                "text": text,
                "font_size": font_size,
                "bold": bold
            })
    return lines

def is_heading(text, font_size, bold):
    stripped = text.strip().lower()
    word_count = len(text.split())

    if stripped in HEADING_HINTS:
        return True
    if text.endswith(":") and word_count <= 7:
        return True
    if bold and word_count <= 6:
        return True
    if font_size >= 14 and word_count <= 6:
        return True
    return False

# --- Main Extraction ---
def extract_chunks():
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout)
        writer.writerow(["type", "text", "font_size", "bold", "page", "document"])

        for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
            doc = fitz.open(pdf_path)
            print(f"📄 Processing {pdf_path.name} ...")

            for page_number, page in enumerate(doc):
                lines = extract_lines_from_page(page)
                previous_was_heading = False

                for line in lines:
                    text = line["text"]
                    font_size = line["font_size"]
                    bold = line["bold"]

                    is_head = is_heading(text, font_size, bold)

                    # Downgrade consecutive headings
                    if is_head:
                        if previous_was_heading:
                            line_type = "BODY"
                        else:
                            line_type = "HEADING"
                            previous_was_heading = True
                    else:
                        line_type = "BODY"
                        previous_was_heading = False

                    writer.writerow([
                        line_type, text, font_size, bold, page_number + 1, pdf_path.name
                    ])
            doc.close()

    print(f"\n✅ Extraction completed. Output saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    extract_chunks()