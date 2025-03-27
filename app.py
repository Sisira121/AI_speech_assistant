import whisper
import numpy as np
import sounddevice as sd
import wave
import google.generativeai as genai
import tempfile
import os
import streamlit as stimport streamlit as st
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(key="speech")


# Load Whisper model
model = whisper.load_model("base")

# Set up Google Gemini API
genai.configure(api_key="AIzaSyDiOwk3wZ4vFFNIUzbLrk_2LbdsLovh-7E")

# Audio recording parameters
CHANNELS = 1
RATE = 16000  # Whisper prefers 16kHz
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 15  # Length of each recording chunk

def record_audio():
    """Records audio and saves it as a temporary file."""
    
    # Initialize and start the stream inside the function
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16', blocksize=CHUNK) as stream:
        frames = []
        for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data, overflowed = stream.read(CHUNK)
            frames.append(data)

    # Convert recorded frames to bytes
    audio_data = np.concatenate(frames, axis=0).tobytes()

    # Save recorded audio as a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        with wave.open(temp_audio.name, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 16-bit PCM (2 bytes per sample)
            wf.setframerate(RATE)
            wf.writeframes(audio_data)
        return temp_audio.name

# Function to query Google Gemini
def ask_gemini(question):
    """Queries Google Gemini API and returns the response."""
    system_prompt = """
    The user is an AI engineer with expertise in OCR, NLP, AI agents, Generative AI, RAG, and deep learning.
    Act as a highly knowledgeable AI mentor and respond with structured, insightful, and technical depth.
    Use bullet points or step-by-step explanations when needed. Ensure responses are practical, concise, and relevant to real-world AI applications.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(system_prompt + "\nUser Query: " + question)
    return response.text if response else "Sorry, I couldn't understand."

# Streamlit UI
st.set_page_config(page_title="AI Speech Assistant", page_icon="🎙️", layout="wide")
st.title("🎤 AI Speech-to-Text & Chatbot")
st.markdown("## Speak, Transcribe, and Chat with AI 🤖")
st.write("Click the button below to record your voice. The AI will transcribe it and generate a response!")

# UI Design
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 10px;
        }
        .stAlert {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Record & Process Audio
if st.button("🎙️ Start Recording"):
    st.write("🔴 Recording... Speak now!")
    audio_file = record_audio()
    
    if audio_file:
        st.success("✅ Recording Complete!")
        st.write("🔍 Transcribing...")
        result = model.transcribe(audio_file, language="en")
        question = result["text"]
        st.info(f"🗣️ You said: {question}")
        os.remove(audio_file)  # Cleanup
        
        # Query AI model
        st.write("🤖 Thinking...")
        response = ask_gemini(question)
        st.success(f"💡 AI Response: {response}")
