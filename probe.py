import ffmpeg

def duration_of_audio(audio_file):
    try:
        probe = ffmpeg.probe(audio_file)
        audio_stream = None
        for stream in probe.get('streams', []):
            if stream.get('codec_type') == 'audio':
                audio_stream = stream
                break

        if audio_stream:
            duration_ts = audio_stream.get('duration_ts')
            sample_rate = audio_stream.get('sample_rate')
            if duration_ts is not None and sample_rate:
                return float(duration_ts) / float(sample_rate)

            stream_duration = audio_stream.get('duration')
            if stream_duration is not None:
                return float(stream_duration)

        return float(probe['format']['duration'])
    except Exception as e:
        print(f"Error probing audio file: {e}")
        return None