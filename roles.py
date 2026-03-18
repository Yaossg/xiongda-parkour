import json

def load_roles_data():
    with open("in/roles.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        voice_ids = [item['voice_id'] for item in data]
        labels = [item['label'] for item in data]
        colors = [item['color'] for item in data]
        return voice_ids, labels, colors