import csv
import os
from typing import List, Dict, Any

DATA_DIR = "localdata"

def verify_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_csv_path(filename: str) -> str:
    verify_dir()
    return os.path.join(DATA_DIR, filename)

def read_csv(filename: str) -> List[Dict[str, Any]]:
    path = get_csv_path(filename)
    if not os.path.exists(path):
        return []
    
    if os.path.getsize(path) == 0:
        return []
        
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return []
        return [row for row in reader if row]

def write_csv(filename: str, data: List[Dict[str, Any]], fieldnames: List[str]):
    path = get_csv_path(filename)
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def get_next_id(filename: str) -> int:
    rows = read_csv(filename)
    if not rows:
        return 1
    ids = [int(row["id"]) for row in rows if "id" in row and str(row["id"]).isdigit()]
    return max(ids) + 1 if ids else 1