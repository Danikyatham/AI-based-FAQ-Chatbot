from flask import Flask, request, jsonify, render_template
import os
import speech_recognition as sr
import random

app = Flask(__name__)

# Mini Daniel interview-style responses
responses = {
    # Personal introduction
    "what is your name":"my name is Daniel , how can i help you",
    "tell me about yourself": "I am Daniel, and I specialize in analyzing data to solve business problems. I have experience with Excel, SQL, and Python, and I enjoy building projects that showcase my skills.",

    # Experience
    "what is your experience": "I have hands-on experience in data analysis, working with datasets to extract meaningful insights and generate reports for decision making.",
    "tell me about your projects": "I have worked on projects including analyzing sales data, predicting trends using SQL and Python, and creating dashboards in Excel.",

    # Skills
    "what are your skills": "I am skilled in SQL, Excel, Python, and data visualization. I can clean, manipulate, and analyze datasets efficiently.",
    "what tools do you use": "I mainly use Python, SQL, and Excel, along with libraries like pandas, matplotlib, and numpy for analysis.",

    # Motivation / Soft skills
    "why do you want this job": "I am eager to apply my analytical skills to real-world business problems and contribute meaningfully to the team.",
    "why should we hire you": "Because I combine strong technical skills with a problem-solving mindset and a passion for turning data into actionable insights.",
#
    "who created you" : " i have been developed by mr.Daniel",
    "who are you": "I am Daniel, a passionate Data Analyst with a Master's in Computer Applications. I enjoy transforming data into actionable insights.",

    #details
    "what is your email": "You can reach me at: daniikyatham@gmail.com",
    "your email": "My email is: daniikyatham@gmail.com",
    "share your email": "Sure! Here’s my email: daniikyatham@gmail.com",

    "what is your phone number": "You can contact me at: 9014663074",
    "your contact number": "My contact number is: 9014663074",
    "your number": "My contact number is: 9014663074",
    "share your number": "Sure! Here’s my phone number: 9014663074",

    # Greetings / small talk
    "hey":"Hello! How can I assist you today?",
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! Ready to talk about data and analysis?",
    "bye": "Goodbye! It was great talking to you."
}

# Generic fallback responses for unrecognized input
fallback_responses = [
    "Could you please rephrase the question?",
    "Could you clarify your question?",
    "Interesting! Could you ask that differently?",
    "sorry, i can't get it but , You can also contact me directly at: daniikyatham@gmail.com",
    "hmm..,sorry, i can't get it , but You can also contact me directly @ 9014663074"

]

def get_response(user_input):
    user_input_lower = user_input.lower()
    for key in responses:
        if key in user_input_lower:
            return responses[key]
    return random.choice(fallback_responses)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    print("Received data:", data)  # Debug

    if data is None:
        return jsonify({'error': 'No JSON data received.'}), 400

    if 'message' in data:
        user_message = data['message']
        bot_response = get_response(user_message)
        return jsonify({'bot_response': bot_response})
    else:
        return jsonify({'error': 'Invalid request'}), 400

def transcribe_voice(voice_data, sample_rate=None, sample_width=None):
    try:
        r = sr.Recognizer()
        with sr.AudioData(voice_data, sample_rate=sample_rate, sample_width=sample_width) as source:
            audio = r.record(source)
        transcription = r.recognize_google(audio)
        return transcription if transcription else ""  # Return empty string if None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

if __name__ == '__main__':
    app.run(debug=True)
