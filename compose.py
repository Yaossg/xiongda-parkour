import json
import ffmpeg

from parser import parse_dialog
from probe import duration_of_audio
from subtitle import generate_subtitles, subtitle_to_ass
from roles import load_roles_data

roles = load_roles_data()

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

def create_talking_overlay(role_id, role, subtitles, duration):
    image_stream = (
        ffmpeg.input(f"in/{role.talking}", t=duration)
        .video
        .filter("scale", role.width, role.height)
    )

    enable_expr = "+".join([f"between(t,{subtitle['start']},{subtitle['end']})" for subtitle in subtitles if subtitle['role_id'] == role_id])
    
    return image_stream, enable_expr

def create_thinking_overlay(role_id, role, subtitles, duration):
    image_stream = (
        ffmpeg.input(f"in/{role.thinking}", t=duration)
        .video
        .filter("scale", role.width, role.height)
    )

    enable_expr = "+".join([f"between(t,{subtitle['start']},{subtitle['end']})" for subtitle in subtitles if subtitle['role_id'] != role_id])
    
    return image_stream, enable_expr


def render_video(video_file, subtitles, subtitles_file, output_file):
    duration = duration_of_audio(video_file)
    video_input = ffmpeg.input(video_file)
    audio_input = ffmpeg.input(video_file)
    for (role_id, role) in enumerate(roles):
        image_stream, enable_expr = create_talking_overlay(role_id, role, subtitles, duration)
        video_input = ffmpeg.overlay(video_input, image_stream, x=role.x, y=role.y, enable=enable_expr)
        image_stream, enable_expr = create_thinking_overlay(role_id, role, subtitles, duration)
        video_input = ffmpeg.overlay(video_input, image_stream, x=role.x, y=role.y, enable=enable_expr)

    video_input = video_input.filter("subtitles", subtitles_file)
    output = ffmpeg.output(video_input, audio_input, output_file, vcodec='libx264', acodec='aac').overwrite_output()
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

    render_video("out/video_with_audio.mp4", subtitles, "out/subtitles.ass", "out/final_video.mp4")