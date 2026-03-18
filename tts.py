import os
import time
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
import env
import uuid
import json

from roles import load_roles_data

dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

TARGET_MODEL = "cosyvoice-v3.5-plus"

voice_ids, labels, _ = load_roles_data()

def tts(voice_index, text_to_synthesize):
    try:
        voice_id = voice_ids[voice_index]
        synthesizer = SpeechSynthesizer(model=TARGET_MODEL, voice=voice_id)
        
        audio_data = synthesizer.call(text_to_synthesize)
        print(f"Speech synthesis successful. Request ID: {synthesizer.get_last_request_id()}")

        tts_id = uuid.uuid4()
        
        with open(f"out/{tts_id}.json", "w", encoding='utf-8') as f:
            json.dump({
                "voice_id": voice_id,
                "label": labels[voice_index],
                "request_id": synthesizer.get_last_request_id(),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                "input_text": text_to_synthesize
            }, f, ensure_ascii=False, indent=4)

        output_file = f"out/{tts_id}.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        
        print(f"Audio saved to {output_file}")
        return tts_id
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return None
