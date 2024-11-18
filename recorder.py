from pydub import AudioSegment
import soundfile as sf
import soundcard as sc
import numpy as np
import subprocess
import threading
import warnings
import time
import mss
import cv2
import os


def calculate_db(samples, ref=32768):
    # Calculate the decibel (dB) levels for the given audio samples.
    rms = np.sqrt(np.mean(np.square(samples)))  # Root Mean Square
    if rms == 0:
        return -np.inf  # Handle silent audio
    return 20 * np.log10(rms / ref)


def analyze_audio(audio_path):
    # Analyze the audio file and calculate Lowest Volume, Highest Peak, and Average Volume in dB.
    audio = AudioSegment.from_file(audio_path)

    # Convert audio samples to numpy array
    samples = np.array(audio.get_array_of_samples(), dtype=float)
    ref = 32768  # Maximum amplitude for 16-bit audio

    # Calculate dB values
    lowest_db = 20 * np.log10(np.abs(samples.min()) / ref) if samples.min() != 0 else -np.inf
    highest_db = 20 * np.log10(np.abs(samples.max()) / ref)
    average_db = calculate_db(samples, ref)

    return lowest_db, highest_db, average_db


def record_screen(record_time: int, output_folder="Recordings") -> str:
    warnings.filterwarnings("ignore")

    # Event to stop recording
    stop_recording = threading.Event()

    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Setup for screen capture
    sct = mss.mss()
    screen = sct.monitors[1]
    frames = []

    # Record audio in parallel
    def record_audio(output_file=os.path.join(output_folder, "out.mp3"), sample_rate=44100, chunk_duration=1):
        data = []
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
            while not stop_recording.is_set():
                chunk = mic.record(numframes=sample_rate * chunk_duration)
                data.append(chunk[:, 0])
        full_data = np.concatenate(data, axis=0)
        sf.write(file=output_file, data=full_data, samplerate=sample_rate)

    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    # Record video
    start_time = time.time()
    while time.time() - start_time < record_time:
        if stop_recording.is_set():
            break
        img = sct.grab(screen)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frames.append(frame)

    stop_recording.set()
    audio_thread.join()

    # Save video with frames and audio
    fps = len(frames) / record_time
    frames_dir = os.path.join(output_folder, "frames")
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    for i, frame in enumerate(frames):
        cv2.imwrite(os.path.join(frames_dir, f"frame_{i:04d}.png"), frame)

    output_video_file = os.path.join(output_folder, f"Recording_{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp4")
    subprocess.run([
        "ffmpeg",
        "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%04d.png",
        "-i", os.path.join(output_folder, "out.mp3"),
        "-shortest",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_video_file
    ])

    # Cleanup
    for file in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, file))
    os.rmdir(frames_dir)
    os.remove(os.path.join(output_folder, "out.mp3"))

    # Analyze audio after saving the video
    audio_file = os.path.join(output_folder, "out.mp3")
    extracted_audio = os.path.join(output_folder, "extracted_audio.wav")

    # Extract audio from the video
    subprocess.run([
        "ffmpeg", "-i", output_video_file, "-q:a", "0", "-map", "a", extracted_audio
    ])

    lowest_db, highest_db, average_db = analyze_audio(extracted_audio)
    print(f"Audio Analysis Results (in dB):\n"
          f"Lowest Volume: {lowest_db:.2f} dB\n"
          f"Highest Peak: {highest_db:.2f} dB\n"
          f"Average Volume: {average_db:.2f} dB")

    return output_video_file
