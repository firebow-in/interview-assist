import os
import shutil
import uuid
try:
    from moviepy import VideoFileClip
except ImportError:
    # Older version fallback
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        VideoFileClip = None

# Ensure input directory exists
INPUT_DIR = os.path.join("data", "input")
os.makedirs(INPUT_DIR, exist_ok=True)

def extract_audio(video_input):
    """
    Extracts audio from a video file into a local MP3.
    """
    if not video_input:
        return None
        
    # Standard Gradio returns a path string, but sometimes it might be a dict (old versions)
    # Ensure we have a string path
    original_file_path = video_input if isinstance(video_input, str) else video_input.get("name")
    
    if not original_file_path or not os.path.exists(original_file_path):
        print(f"Error: Original file not found at {original_file_path}")
        return None

    # Step 1: Stage file locally to bypass permission issues with temporary system folders
    file_ext = os.path.splitext(original_file_path)[1]
    local_video_name = f"video_{uuid.uuid4().hex}{file_ext}"
    local_video_path = os.path.join(INPUT_DIR, local_video_name)
    
    try:
        shutil.copy2(original_file_path, local_video_path)
    except Exception as e:
        print(f"Failed to copy file to local storage: {e}")
        local_video_path = original_file_path

    # If it's already an audio file, just return the local copy path
    if local_video_path.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
        return local_video_path

    # Define output audio path
    audio_output_path = os.path.splitext(local_video_path)[0] + ".mp3"

    video = None
    try:
        if VideoFileClip is None:
            raise ImportError("MoviePy not found")
            
        print(f"Extracting audio using MoviePy from {local_video_path}")
        video = VideoFileClip(local_video_path)
        
        # Use a unique temp audio file to avoid collisions
        temp_audio = os.path.join(INPUT_DIR, f"temp_{uuid.uuid4().hex}.mp3")
        
        video.audio.write_audiofile(
            audio_output_path, 
            verbose=False, 
            logger=None,
            temp_audiofile=temp_audio
        )
        return audio_output_path
        
    except Exception as e:
        print(f"MoviePy extraction failed: {e}. Fallback to original path.")
        return local_video_path
        
    finally:
        if video:
            try:
                video.close()
            except:
                pass

def get_playable_video(video_path):
    """
    Ensures video is in a browser-supported H.264/AAC format.
    Required for compatibility across different browsers and Gradio's video player.
    """
    if not video_path or not os.path.exists(video_path):
        return None
    
    output_path = os.path.splitext(video_path)[0] + "_playable.mp4"
    
    video = None
    try:
        if VideoFileClip is None:
            return video_path
            
        print(f"Re-encoding video for playability: {video_path}")
        video = VideoFileClip(video_path)
        
        # Standard H.264 + AAC is very browser-compatible
        video.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac",
            verbose=False, 
            logger=None
        )
        return output_path
        
    except Exception as e:
        print(f"Re-encoding failed: {e}")
        return video_path
    finally:
        if video:
            try:
                video.close()
            except:
                pass