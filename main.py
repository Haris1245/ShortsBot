from moviepy.editor import *
from openai import OpenAI
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
from pytube import YouTube
import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import random
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe"})

client = OpenAI(api_key="api_key")

colors = [
    "green",
    "yellow",
    "red",
    "white"
]
fonts = [
    "Impact",
    "Comic-Sans-MS",
    "Arial"
]




def Download(link):
    try:
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        filename = youtubeObject.default_filename  # Get the default filename
        youtubeObject.download()
        print("Download is completed successfully")
        return filename
    except Exception as e:
        print("An error has occurred:", e)
        return None
    
    
def get_subs(clip):
    # Extract audio from the video clip
    audio = clip.audio
    audio.write_audiofile("subs.wav")
    
    # Transcribe audio using OpenAI's API
    audio_file = open("subs.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )
    
    # Extract text and timing information
    text = transcript.text
    timestamps = transcript.words
    
    # Return text and timing information
    return {'text': text, 'timestamps': timestamps}



def generate_subtitles_clip(subs, delay=0.05):
    # Extract text and timing information
    text = subs['text']
    timestamps = subs['timestamps']
    
    # Generate subtitle clips with timings
    clips = []
    for word_info in timestamps:
        start_time = word_info['start'] + delay  # Add delay to start time
        end_time = word_info['end'] + delay      # Add delay to end time
        word = word_info['word']
        clips.append(((start_time, end_time), word.upper()))  # Include text alongside timings
    
        font = random.choice(fonts)
        color = random.choice(colors)
    return SubtitlesClip(clips, lambda txt: TextClip(txt, fontsize=100, color=color, method='caption', stroke_color="black", stroke_width=6, font=font))


# Load your video clip
def generate_video(video_p, count):
    video_path = video_p
    video = VideoFileClip(video_path).subclip(748, 776).fx(vfx.fadeout, 1)
    logo  = ImageClip("logo.png").resize(width=150)
    # Calculate the aspect ratio of the video
    aspect_ratio = video.size[0] / video.size[1]

    # Calculate the dimensions for cropping
    if aspect_ratio > 9/16:  # Video is wider than 9:16
        new_width = int(9/16 * video.size[1])
        crop_x = (video.size[0] - new_width) / 2
        crop_y = 0
        video = video.crop(x1=crop_x, y1=crop_y, x2=crop_x + new_width, y2=video.size[1])
    else:  # Video is taller than 9:16
        new_height = int(16/9 * video.size[0])
        crop_x = 0
        crop_y = (video.size[1] - new_height) / 2
        video = video.crop(x1=crop_x, y1=crop_y, x2=video.size[0], y2=crop_y + new_height)

    # Resize the video to fit 1080x1920 (9:16 aspect ratio)
    video = video.resize(height=1920)
    # Generate subtitles
    subs_result = get_subs(video)

    # Create SubtitlesClip with timings
    subs_clip = generate_subtitles_clip(subs_result)

    # Overlay subtitles on the video
    final_video = CompositeVideoClip([video.set_duration(subs_clip.duration), subs_clip.set_position(((1920/2 - 1080/2 ) , 1200)), logo.set_position(("right", "top")).set_duration(subs_clip.duration)])

    # Write the final video file
    final_video.write_videofile(f"output_video{count}.mp4", fps=24)
count = 2

while True:
    link = input("Enter the YouTube video URL: ")
    file_name = Download(link)
    generate_video(file_name, count)
    count += 1 
    if link == "exit":
        break