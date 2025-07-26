
import json
from pathlib import Path
from typing import Any, TypeAlias, Union

STR_PATH: TypeAlias = Union[str, Path]

def save_json(path: STR_PATH, data: Union[dict, list]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(path: STR_PATH, default: Union[dict, list] = {}) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default
    except FileNotFoundError:
        return default
