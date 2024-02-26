
# ShortsBot

This project creates YouTube shorts from long form videos by giving it a link.



## Setup

First in the main.py file you put in place of "api_key" in the OpenAI Client you put your api_key or do it through env variable I had problems that is why I didn't do it like that and when you run the main.py there is an input where you paste the link of the video and in the code where  video = VideoFileClip(video_path).subclip(748, 776) in place of the numbers you put the seconds you want the shorts to be between! And it will create the short for you. 

## Features

- Right now I am working that the bot can recognize where the  face is and make 9:16 frame where it is the code for that is in tracking_face.py its in very early stages, so you can contribute if you can!

