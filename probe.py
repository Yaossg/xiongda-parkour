import ffmpeg

def duration_of_audio(audio_file):
    try:
        probe = ffmpeg.probe(audio_file)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"Error probing audio file: {e}")
        return None