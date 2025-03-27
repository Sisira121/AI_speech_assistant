import whisper
import pyaudio
import numpy as np
import wave
import google.generativeai as genai
import tempfile
import os
import pyttsx3
import streamlit as st

# Load Whisper model
model = whisper.load_model("base")

# Set up Google Gemini API
genai.configure(api_key="AIzaSyDiOwk3wZ4vFFNIUzbLrk_2LbdsLovh-7E")



# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper prefers 16kHz
CHUNK = 1024  # Buffer size
SILENCE_THRESHOLD = 500  # Adjust for noise levels
RECORD_SECONDS = 15  # Length of each recording chunk

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Listening for speech...")

def record_audio():
    """Records a chunk of audio and saves it as a temporary file."""
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Save recorded audio as a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        wf = wave.open(temp_audio.name, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()
        return temp_audio.name

# Function to query Google Gemini
def ask_gemini(question):
    """Queries Google Gemini API and returns the response."""
    system_prompt = """
    The user is an AI engineer with expertise in OCR, NLP, AI agents, Generative AI, RAG, and deep learning.
    Act as a highly knowledgeable AI mentor and respond with structured, insightful, and technical depth. Use bullet points or step-by-step explanations when needed. Ensure responses are practical, concise, and relevant to real-world AI applications.
    Only answer the question asked without displaying the entire prompt.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(system_prompt + "\nUser Query: " + question)
    return response.text if response else "Sorry, I couldn't understand."
    


def speak_text(text):
    """Converts text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()


# Streamlit UI
st.set_page_config(page_title="AI Speech Assistant", page_icon="🎙️",layout= "wide")
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
        




