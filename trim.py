import ffmpeg

def trim_slicene(input_file, output_file):
    # silenceremove=window=0:detection=peak:stop_mode=all:start_mode=all:stop_periods=-1:stop_threshold=0
    input_stream = ffmpeg.input(input_file)
    output_stream = input_stream.filter("silenceremove", window=0, detection="peak", stop_mode="all", start_mode="all", stop_periods=-1, stop_threshold=0)
    output = ffmpeg.output(output_stream, output_file, acodec="pcm_s16le").overwrite_output()
    ffmpeg.run(output)

def trim_all(speech_ids):
    for speech_id in speech_ids:
        input_file = f"out/{speech_id}.mp3"
        output_file = f"out/{speech_id}_trimmed.wav"
        trim_slicene(input_file, output_file)