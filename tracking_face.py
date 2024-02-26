import cv2
import moviepy.editor as mp
import numpy as np

def detect_faces(video_path, target_size, min_neighbors=20, min_size=(80, 80), frame_update_interval=10):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    region = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB (for moviepy compatibility)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces every frame_update_interval frames or if no region is defined
        if frame_count % frame_update_interval == 0 or region is None:
            # Detect faces
            faces = face_cascade.detectMultiScale(rgb_frame, scaleFactor=1.1, minNeighbors=min_neighbors, minSize=min_size)

            if len(faces) > 0:
                # Get the first detected face (you may adjust this logic)
                x, y, w, h = faces[0]

                # Calculate the region around the detected face
                region_x = max(0, x - w // 2)
                region_y = max(0, y - h // 4)
                region_w = min(frame.shape[1] - region_x, w * 3)
                region_h = min(frame.shape[0] - region_y, h * 3)

                # Store the region
                region = (region_x, region_y, region_w, region_h)

        if region is not None:
            # Extract the region around the detected face and resize it
            region_x, region_y, region_w, region_h = region
            face_frame = rgb_frame[region_y:region_y+region_h, region_x:region_x+region_w].copy()
            face_frame = cv2.resize(face_frame, target_size)

            frames.append(face_frame)

        frame_count += 1

    cap.release()
    return frames

def save_video(frames, output_path, video_path, fps, size):
    # Load the video to get its duration
    video_clip = mp.VideoFileClip(video_path)
    duration = video_clip.duration
    video_clip.close()
    
    # Adjust frame rate to avoid accessing frames beyond the video duration
    adjusted_fps = min(fps, round(len(frames) / duration))

    clip = mp.ImageSequenceClip(frames, fps=adjusted_fps)
    
    # Extract audio from original video
    audio_clip = mp.AudioFileClip(video_path)
    
    # Match audio duration with video duration
    audio_duration = min(duration, len(frames) / adjusted_fps)
    audio_clip = audio_clip.set_duration(audio_duration)
    
    # Combine video clip with audio clip
    final_clip = clip.set_audio(audio_clip)
    
    # Write final video file
    final_clip.write_videofile(output_path, fps=adjusted_fps, codec='mpeg4', threads=4, preset='ultrafast', ffmpeg_params=['-vf', f'scale={size[0]}:{size[1]}'])

if __name__ == "__main__":
    input_video_path = "input5.mp4"
    output_video_path = "ouuttt.mp4"
    fps = 28
    size = (1080, 1920)  # 9:16 resolution

    frames = detect_faces(input_video_path, size)
    save_video(frames, output_video_path, input_video_path, fps, size)
