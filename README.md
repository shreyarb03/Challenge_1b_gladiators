# Challenge 1B: Persona-Driven Document Intelligence

This repository contains our solution for **Challenge 1B: "Persona-Driven Document Intelligence"** with the theme: **“Connect What Matters — For the User Who Matters”** in the **Adobe India Hackathon**.

The objective is to extract the most relevant sections from a corpus of PDF documents, based on a **given user persona** and a **job-to-be-done**, by applying lightweight language model inference and scoring.

---

## Features

- Uses **PyMuPDF (fitz)** for extracting text from PDFs with font size and boldness information
- Employs a **quantized `phi-1_5` model (Q5_0 GGUF)** for scoring text relevance
- Runs locally using **llama-cpp-python** (no GPU required)
- Fully containerized using Docker for reproducible execution

---

## Getting Started

### 1. Clone the Repository (with Git LFS)

This repository uses Git Large File Storage (LFS) to manage model weights and large files.

```bash
git lfs install
git clone https://github.com/shreyarb03/Challenge_1b_gladiators.git
cd Challenge_1b_gladiators
```

### 2. Prepare Input Files

Place the following files in the root directory (or a mounted volume):

- `Collection/challenge1b_input.json` — Contains the persona and job-to-be-done and metadata.
- `Collection/pdfs` — Folder should contain PDFs for the input.

### Input json structure
```bash
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```
## Running with Docker

### 3. Build the Docker Image

```bash
docker build -t challenge-1b .
```

### 4. Run the Container

```bash
docker run --rm -v "${PWD}/Collection:/Collection" challenge-1b
```


- Output JSON: `Collection/challenge1b_output.json`

---

## Output Format

The output is a single JSON file (`challenge1b_output.json`) with the top-ranked sections from the corpus:

```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

---

## Model Information

- Model: `phi-1_5-Q5_0.gguf` quantized GGUF model (by Microsoft)
- Inference Engine: `llama-cpp-python` for fast, CPU-only local inference
- Scoring Logic: Each extracted line from PDFs is passed with the persona context to the LLM; scores are used to rank and return top relevant snippets
- Extraction: Font-based text segmentation using `PyMuPDF`, stored as CSV before classification

---

## Pipeline Overview

1. `extract_chunks.py` — Parses PDFs and extracts line-wise segments with font size and boldness
2. `score_chunks.py` — Uses a lightweight quantized LLM to score each chunk against the persona and task
3. Final output is saved in structured JSON format

