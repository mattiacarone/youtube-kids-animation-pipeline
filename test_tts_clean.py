"""
Test different clean TTS options without any robotic audio filters.
"""
import os
import win32com.client
from gtts import gTTS
from moviepy import AudioFileClip

TEST_TEXT = "Hello, little explorers! Welcome to Pixieland. Can you say Hello?"

def test_gtts():
    try:
        tts = gTTS(TEST_TEXT, lang='en', tld='com')
        out = "assets/audio/test_gtts_clean.mp3"
        tts.save(out)
        a = AudioFileClip(out)
        print(f"gTTS Clean: Success! Duration = {a.duration:.2f}s")
        a.close()
    except Exception as e:
        print(f"gTTS error: {e}")

def test_sapi5():
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        filestream = win32com.client.Dispatch("SAPI.SpFileStream")
        out = r"C:\Users\Mattia\YouTubeKids\assets\audio\test_sapi5.wav"
        filestream.Open(out, 3, False) # 3 = SSFMCreateForWrite
        speaker.AudioOutputStream = filestream
        speaker.Rate = -1 # slightly slower, pleasant pacing
        speaker.Speak(TEST_TEXT)
        filestream.Close()
        a = AudioFileClip(out)
        print(f"SAPI5 Clean: Success! Duration = {a.duration:.2f}s")
        a.close()
    except Exception as e:
        print(f"SAPI5 error: {e}")

if __name__ == "__main__":
    test_gtts()
    test_sapi5()

