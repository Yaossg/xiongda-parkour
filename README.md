# XIONGDA PARKOUR

熊大熊二 - MC 跑酷视频生成器

## Features

- Text-to-speech dialog synthesis with multiple voices
- Automatic subtitle timing from generated audio
- ASS subtitles with per-role styles/colors
- Audio concatenation and muxing onto a video

## Requirements

- Python 3.9+
- ffmpeg installed and available in PATH
- DashScope API key

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:

```bash
DASHSCOPE_API_KEY=your_api_key_here
```

3. Prepare inputs in the `in/` folder:

- `dialog.txt` with lines in the form `role_id: text`
- `roles.json` with voice ids, labels, and colors
- `video.mp4` as the base video

Example `dialog.txt`:

```text
0: 你到底还是来了。
1: 不是我要来的。
```

Example `roles.json`:

```json
[
	{
		"voice_id": "cosyvoice-...",
		"label": "熊大",
		"color": "003333CC"
	},
	{
		"voice_id": "cosyvoice-...",
		"label": "熊二",
		"color": "0033CCCC"
	}
]
```

## Run

Generate speech audio files:

```bash
python synth.py
```

Compose final outputs (subtitles, combined audio, muxing, final video):

```bash
python compose.py
```

## Outputs

- `out/*.mp3` per-line audio files
- `out/speech_ids.json` list of audio ids
- `out/subtitles.json` subtitle timing data
- `out/subtitles.ass` ASS subtitles
- `out/combined.mp3` concatenated audio
- `out/video_with_audio.mp4` muxed video
- `out/final_video.mp4` final video with burned-in subtitles

## Utilities

- `clean.py` removes files under `out/`
- `list.py` lists available voices from DashScope