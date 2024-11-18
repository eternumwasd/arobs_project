# Project for AROBS Engineering

Simple script in Selenium that opens YouTube, searches for a term, and clicks on the first video it finds. This was the theme provided for the project required to enter the internship.

## Usage:

Install modules using:
```py
pip install -r requirements.txt
```

Additionally, install [FFmpeg](https://www.ffmpeg.org/download.html) and add it to PATH.

## Features

- Takes a search term, enters YouTube automatically, and presses on the first video available.
- Records the screen for a certain amount of time while the video is playing.
- Takes the audio from the video and measures the sound level throughout.
- If there are any ads, the script automatically skips them for you.
