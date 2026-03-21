import json

from probe import duration_of_audio

from parser import parse_dialog

from tts import load_roles_data

roles = load_roles_data()

def generate_subtitles(dialog_list, speech_ids):
    subtitles = []
    current_time = 0.0
    
    for (role_id, content), speech_id in zip(dialog_list, speech_ids):
        audio_file = f"out/{speech_id}.mp3"
        duration = duration_of_audio(audio_file)
        if duration is None:
            print(f"Skipping subtitle for {audio_file} due to probe error.")
            continue
        
        subtitle_entry = {
            "start": round(current_time, 2),
            "end": round(current_time + duration, 2),
            "text": content,
            "role_id": role_id
        }
        subtitles.append(subtitle_entry)
        current_time += duration
    
    with open("out/subtitles.json", "w", encoding='utf-8') as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=4)

    print("Subtitles generated and saved to out/subtitles.json")
    return subtitles


def subtitle_to_ass(subtitles, output_file):
    def format_time(seconds):
        total_centis = int(round(seconds * 100))
        hours = total_centis // (3600 * 100)
        remaining = total_centis % (3600 * 100)
        minutes = remaining // (60 * 100)
        remaining = remaining % (60 * 100)
        secs = remaining // 100
        centis = remaining % 100
        return f"{hours}:{minutes:02}:{secs:02}.{centis:02}"
    
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("[Script Info]\n")
        f.write("Title: Subtitles\n")
        f.write("ScriptType: v4.00+\n")
        f.write("\n[V4+ Styles]\n")
        f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        f.write("Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0.00,1,2.00,0.00,2,10,10,10\n")


        for role in roles:
            f.write(
                "Style: {name},Arial,24,&H{primary},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0.00,1,2.00,0.00,2,10,10,10\n".format(
                    name=role.label,
                    primary=role.color,
                )
            )
        f.write("\n[Events]\n")
        f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            
        for subtitle in subtitles:
            start_time = subtitle['start']
            end_time = subtitle['end']
            text = subtitle['text']
            role_id = subtitle['role_id']
            role = roles[role_id]
            style_name = role.label

            safe_text = str(f"{role.prefix}{text}").replace("{", r"\{").replace("}", r"\}")
            safe_text = safe_text.replace("\n", r"\N")

            f.write(
                "Dialogue: 0,{start},{end},{style},,0,0,0,,{text}\n".format(
                    start=format_time(start_time),
                    end=format_time(end_time),
                    style=style_name,
                    text=safe_text,
                )
            )

    print(f"ASS subtitles saved to {output_file}")


if __name__ == "__main__":
    with open("out/speech_ids.json", "r", encoding='utf-8') as f:
        speech_ids = json.load(f)
    
    with open("in/dialog.txt", "r", encoding='utf-8') as f:
        dialog_list = parse_dialog("in/dialog.txt")
    
    subtitles = generate_subtitles(dialog_list, speech_ids)

    subtitle_to_ass(subtitles, "out/subtitles.ass")