import json
import os

DOSYA_ADI = "data.json"

def load_data():
    if not os.path.exists(DOSYA_ADI):
        return []
    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
