import json
import ffmpeg

from parser import parse_dialog
from probe import duration_of_audio
from subtitle import generate_subtitles, subtitle_to_ass

def concatenate_audios(audio_files, output_file):
    inputs = [ffmpeg.input(f"out/{audio_id}.mp3") for audio_id in audio_files]
    joined = ffmpeg.concat(*inputs, v=0, a=1).node
    output = ffmpeg.output(joined[0], output_file).overwrite_output()
    ffmpeg.run(output)

def mux_audio_with_video(audio_file, video_file, output_file):
    audio_input = ffmpeg.input(audio_file)
    video_input = ffmpeg.input(video_file)

    duration = duration_of_audio("out/combined.mp3")

    output = ffmpeg.output(video_input.video, audio_input.audio, output_file, vcodec='copy', acodec='aac', t=duration).overwrite_output()
    ffmpeg.run(output)

def render_subtitles_on_video(video_file, subtitles_file, output_file):
    input_video = ffmpeg.input(video_file)
    output = ffmpeg.output(input_video.video, input_video.audio, output_file, vf=f"subtitles={subtitles_file}", vcodec='libx264', acodec='aac').overwrite_output()
    ffmpeg.run(output)

if __name__ == "__main__":
    with open("out/speech_ids.json", "r", encoding='utf-8') as f:
        speech_ids = json.load(f)
    
    with open("in/dialog.txt", "r", encoding='utf-8') as f:
        dialog_list = parse_dialog("in/dialog.txt")
    
    subtitles = generate_subtitles(dialog_list, speech_ids)
    
    subtitle_to_ass(subtitles, "out/subtitles.ass")
    
    concatenate_audios(speech_ids, "out/combined.mp3")
    
    mux_audio_with_video("out/combined.mp3", "in/video.mp4", "out/video_with_audio.mp4")

    render_subtitles_on_video("out/video_with_audio.mp4", "out/subtitles.ass", "out/final_video.mp4")