# AI Speech Assistant

## 🎙️ Overview
AI Speech Assistant is a real-time speech-to-text and AI chatbot application built using Whisper for speech recognition, Google Gemini for AI-powered responses, and Streamlit for an interactive UI.

## 🚀 Features
- **Real-time Speech Recognition:** Utilizes OpenAI Whisper for accurate speech-to-text conversion.
- **AI-Powered Responses:** Queries Google Gemini API to generate structured, insightful responses.
- **Streamlit UI:** Provides an interactive web-based interface for users to record and process speech.
- **Text-to-Speech (TTS) Engine:** Converts AI-generated responses into speech output (Feature planned).

## 🛠️ Technologies Used
- **Python**
- **Whisper** (Speech recognition)
- **PyAudio** (Audio processing)
- **Wave** (Audio file handling)
- **Google Gemini API** (AI text generation)
- **Streamlit** (Web-based UI)
- **pyttsx3** (Text-to-Speech, planned for future enhancements)

## 📌 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/ai-speech-assistant.git
   cd ai-speech-assistant
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration
Before running the application, configure the **Google Gemini API key** by setting up an environment variable:

```bash
export GOOGLE_GEMINI_API_KEY="your-api-key"
```
(Replace `your-api-key` with your actual Google Gemini API key.)

## ▶️ Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

### How It Works:
1. Click the **"Start Recording"** button to capture audio.
2. The app records your voice and transcribes it using Whisper.
3. The transcribed text is sent to the Google Gemini API for a response.
4. The AI-generated response is displayed on the UI.

## 🔧 Future Improvements
- Implement **text-to-speech (TTS)** functionality using `pyttsx3`.
- Enhance noise filtering for better audio processing.
- Expand support for multiple languages.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## 📜 License
This project is licensed under the MIT License.



