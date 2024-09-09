from flask import Flask, request, jsonify, render_template
import os
import speech_recognition as sr

app = Flask(__name__)

# Predefined chatbot responses
responses = {
    "hi": "hello",
    "hi.": "hello",
    "hello": "hello",
    "hello.": "hello",
    "how are you?": "I'm doing well, thank you!",
    "how are you": "I'm doing well, thank you!",
    "what is your name?": "I'm a chatbot!",
    "what is your name": "I'm a chatbot!",
    "bye": "Goodbye!",
    "fuck you":"fuck you too user",
    "hello chatbot.": "hello user",
    "hi chatbot.": "hello user, how can I assist you today",
    "hi chat bot.": "hello user, how can I assist you today!",
    "hi chatbot": "hello user, how can I help you today",
    "who created you?": "I have been developed by Mr. Daniel."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    if not data:
        return jsonify({'error': 'No JSON data received.'}), 400
    
    user_message = data.get('message', '').strip().lower()
    if not user_message:
        return jsonify({'error': 'Message is empty.'}), 400
    
    bot_response = responses.get(user_message, "I'm not sure how to respond to that.")
    return jsonify({'bot_response': bot_response})

def transcribe_voice(voice_data, sample_rate=None, sample_width=None):
    try:
        r = sr.Recognizer()
        audio_data = sr.AudioData(voice_data, sample_rate, sample_width)
        transcription = r.recognize_google(audio_data)
        return transcription if transcription else ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

if __name__ == '__main__':
    app.run(debug=True)
