
#!! Abbott sensitive data removed. HTML and CSS specific to IBM Maximo !!

import re
from pathlib import Path
from pypdf import PdfReader
import os

def read_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    texts = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        texts.append(t)
    # Join with newlines to preserve boundaries but allow regex to span lines
    return "\n".join(texts)

def find_first(patterns, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL):
    """Try multiple regex patterns; return the first captured group found."""
    for pat in patterns:
        m = re.search(pat, text, flags)
        if m:
            # Return first non-empty capturing group
            for g in m.groups():
                if g and g.strip():
                    return g.strip()
    return None

def normalize_simple(value: str | None) -> str | None:
    if value is None:
        return None
    # Normalize common capitalization for status-like fields
    v = value.strip()
    # Keep original if you prefer; here we title-case 'pass', etc.
    return v[0].upper() + v[1:].lower() if v.lower() in {"pass", "fail"} else v

def extract_calibration_fields(pdf_path: str) -> dict:
    text = read_pdf_text(pdf_path)

    # Common flexible tokens
    sep = r"[:\-–—]"               # colon or dash-like separators
    ws = r"\s*"                     # optional whitespace
    val = r"(.+?)"                  # lazily capture a value

    # Asset Id — often "Asset Id P-4258"
    asset_id = find_first([
        rf"Asset\s*Id{ws}{val}(?:\n|$)",      # no explicit separator in some files
        rf"Asset\s*Id{ws}{sep}{ws}{val}",
    ], text)

    # As found — may appear as "As found-Passed <name> <date>" on Page 1
    as_found = find_first([
        rf"As\s*found{ws}{sep}{ws}([A-Za-z]+)",       # capture single word like Pass/Fail
        rf"As\s*found{ws}{val}",                      # fallback: capture first token(s)
    ], text)
    as_found = normalize_simple(as_found)

    # As left — may appear as "As left-Passed <name> <date>" on Page 2
    as_left = find_first([
        rf"As\s*left{ws}{sep}{ws}([A-Za-z]+)",
        rf"As\s*left{ws}{val}",
    ], text)
    as_left = normalize_simple(as_left)

    # Preventive Maintenance — e.g., "Preventive Maintenance: Piston cleaned and re-greased"
    preventive_maintenance = find_first([
        rf"Preventive\s*Maintenance{ws}{sep}{ws}{val}(?:\n|$)",
        rf"Preventive\s*Maintenance{ws}{val}(?:\n|$)",
    ], text)

    # Adjustment — e.g., "Adjustment: No-Adjustment made"
    adjustment = find_first([
        rf"Adjustment{ws}{sep}{ws}{val}(?:\n|$)",
        rf"Adjustment{ws}{val}(?:\n|$)",
    ], text)

    # Post-process to trim trailing names/dates if they follow "As found/As left"
    # We only want the first token Pass/Fail.
    def first_status_word(s):
        if not s:
            return s
        m = re.match(r"([A-Za-z]+)", s)
        return m.group(1).capitalize() if m else s

    as_found = first_status_word(as_found)
    as_left  = first_status_word(as_left)

    return {
        "asset_id": asset_id,
        "as_found": as_found,
        "as_left": as_left,
        "preventive_maintenance": preventive_maintenance,
        "adjustment": adjustment,
    }

if __name__ == "__main__":
    folder_path = "path_to_folder"
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        result = extract_calibration_fields(file_path)
        print(result)
        
