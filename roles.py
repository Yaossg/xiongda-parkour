import json
from dataclasses import dataclass

@dataclass
class Role:
    voice_id: str
    label: str
    color: str
    prefix: str

def load_roles_data() -> list[Role]:
    with open("in/roles.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        return [Role(**item) for item in data]