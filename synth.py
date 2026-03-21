
from tts import tts
from parser import parse_dialog
import json

def synthesize_dialog(dialog_list):
    speeches = []
    for role_id, content in dialog_list:
        retries = 3
        while retries > 0:
            tts_id = tts(role_id, content)
            if tts_id is not None:
                break
            print(f"Retrying... ({3 - retries + 1}/3)")
            retries -= 1
        if tts_id is None:
            return None
        speeches.append(str(tts_id))
    return speeches

def main():
    dialog = parse_dialog("in/dialog.txt")
    speech_ids = synthesize_dialog(dialog)
    if speech_ids is None:
        print("Failed to synthesize all speeches.")
        return
    
    with open("out/speech_ids.json", "w", encoding='utf-8') as f:
        json.dump(speech_ids, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()