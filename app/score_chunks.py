import csv
import json
from pathlib import Path
from datetime import datetime
from llama_cpp import Llama

# --- Configuration ---
MODEL_PATH = "models/phi-1_5-Q5_0.gguf"
INPUT_CSV = "output_chunks.csv"
OUTPUT_JSON = "/Collection/challenge1b_output.json"
TOP_N = 5
INPUT_META = "/Collection/challenge1b_input.json"
with open(INPUT_META, "r", encoding="utf-8") as f:
    input_data = json.load(f)

PERSONA = input_data["persona"]["role"]
JOB = input_data["job_to_be_done"]["task"]
DOCUMENTS = [doc["filename"] for doc in input_data["documents"]]

# --- Load Model ---
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=32  # Optional for Apple M-series
)

PROMPT_TEMPLATE = """
You are a {persona}. Your task is: {job}

Rate the relevance of the following text to your task on a scale of 1 (most relevant) to 5 (least relevant).
Only respond with a single digit between 1 and 5.

Text:
{text}
"""

def score_text(text):
    prompt = PROMPT_TEMPLATE.format(persona=PERSONA, job=JOB, text=text)
    try:
        response = llm(prompt, max_tokens=10, temperature=0.2)
        result = response["choices"][0]["text"].strip()
        for word in result.split():
            if word.isdigit():
                return max(1, min(int(word), 5))
    except Exception as e:
        print(f" Error scoring text: {e}")
    return 5  # Default to least relevant if failure

# --- Load chunks from CSV ---
with open(INPUT_CSV, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    all_chunks = [row for row in reader]

# --- Step 1: Score headings ---
scored_headings = []
for i, row in enumerate(all_chunks):
    if row["type"] != "HEADING":
        continue
    score = score_text(row["text"])
    scored_headings.append({
        "document": row["document"],
        "section_title": row["text"].strip(),
        "score": score,
        "page_number": int(row["page"]),
        "row_index": i
    })

# --- Step 2: Rank and select top N headings ---
scored_headings.sort(key=lambda h: h["score"])
top_headings = scored_headings[:TOP_N]

# --- Step 3: Collect BODY chunks under each top heading ---
subsection_analysis = []

for rank, heading in enumerate(top_headings, start=1):
    current_doc = heading["document"]
    current_page = heading["page_number"]
    start_index = heading["row_index"]

    collected_text = []
    for row in all_chunks[start_index + 1:]:
        if row["document"] != current_doc:
            continue
        if int(row["page"]) != current_page:
            continue
        if row["type"] == "HEADING":
            break
        text = row["text"].strip()
        if text:
            collected_text.append(text)

    if collected_text:
        subsection_analysis.append({
            "document": current_doc,
            "refined_text": " ".join(collected_text),
            "page_number": current_page
        })

# --- Step 4: Build output JSON ---
output = {
    "metadata": {
        "input_documents": sorted(set([row["document"] for row in all_chunks])),
        "persona": PERSONA,
        "job_to_be_done": JOB,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [
        {
            "document": h["document"],
            "section_title": h["section_title"],
            "importance_rank": rank,
            "page_number": h["page_number"]
        }
        for rank, h in enumerate(top_headings, start=1)
    ],
    "subsection_analysis": subsection_analysis
}

# --- Save output ---
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"\n Done. Output saved to {OUTPUT_JSON}")
