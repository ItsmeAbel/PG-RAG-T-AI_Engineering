# ingestion/load_json.py
import json

#loads json record
def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
