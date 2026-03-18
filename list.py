from dashscope.audio.tts_v2 import VoiceEnrollmentService
import env


service = VoiceEnrollmentService()

voices = service.list_voices(prefix=None, page_index=0, page_size=10)

print(f"Request ID: {service.get_last_request_id()}")
print(f"Found voices: {voices}")
