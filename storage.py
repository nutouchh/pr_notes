import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("notes.json")


def load_notes():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_notes(notes):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)