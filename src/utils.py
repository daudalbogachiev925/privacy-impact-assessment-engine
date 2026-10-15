import yaml
from pathlib import Path
from typing import Any, Dict

def load_yaml(path: str | Path) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary.
    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the file cannot be parsed.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"YAML configuration file not found: {path}")
    with p.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}
