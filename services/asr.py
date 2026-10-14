import os
import whisper

# Path to local models if you have downloaded them manually
LOCAL_MODEL_PATH = os.path.join("data", "models", "base.pt")

def load_whisper_model(name="base"):
    """
    Attempts to load the model from the official location,
    falling back to a local file if available.
    """
    try:
        # Check if local model file exists
        if os.path.exists(LOCAL_MODEL_PATH):
            print(f"Loading Whisper model from local path: {LOCAL_MODEL_PATH}")
            return whisper.load_model(LOCAL_MODEL_PATH)
        
        # Otherwise attempt normal load (which triggers download if not cached)
        print(f"Loading Whisper model: {name} (may attempt download)")
        return whisper.load_model(name)
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("💡 Hint: If you are offline, download 'base.pt' and put it in 'data/models/'.")
        return None

# Load model once at start
model = load_whisper_model("base")

def transcribe(audio_path):
    if model is None:
        return "ERROR: Whisper model not loaded. Check internet connection or provide a local model file."

    try:
        if not audio_path or not os.path.exists(audio_path):
            return f"ERROR: Audio file not found at {audio_path}"
            
        print(f"Transcribing audio: {audio_path}")
        result = model.transcribe(audio_path)
        return result.get("text", "")
        
    except Exception as e:
        print(f"Whisper transcription failed: {e}")
        return f"Error during transcription: {str(e)}"