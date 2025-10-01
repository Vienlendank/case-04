import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Mapping, Any

RESULTS_PATH = Path("data/survey.ndjson")

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def submission_id(record: Mapping[str, Any]) -> str:
    if record.get("submission_id"):
        return record["submission_id"]
    timestamp = datetime.utcnow().strftime("%Y%m%d%H")
    raw = f"{record['email']}{timestamp}"
    return hash_value(raw)

def append_json_line(record: Mapping[str, Any]) -> None:
    
    record["email"] = hash_value(record["email"])
    record["age"] = hash_value(str(record["age"]))
    record["submission_id"] = submission_id(record)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
                default=lambda o: o.isoformat() if isinstance(o, datetime) else o
            ) + "\n"
        )