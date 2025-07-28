#!/bin/bash

set -e

# Print a timestamped header
step() {
  echo -e "\n\033[1;34m  STEP:\033[0m $1"
}

step "Extracting structured chunks from PDFs"
python extract_chunks.py

step "Scoring and selecting relevant sections with LLM"
python score_chunks.py
