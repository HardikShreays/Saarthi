from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle as pk
import os
from http.client import responses
import google.generativeai as genai
import os


load_dotenv()

def send_message(query):
  response = chat_session.send_message(query).text
  history.append({
    "role": "user",
    "parts": [query]
  })
  with open('history.bin',"wb") as hfl :
    pk.dump(history,hfl)

  return response

# print(os.environ.get("API"))
genai.configure(api_key=os.environ.get("API"))
# genai.configure(api_key="AIzaSyAPkzLPXlAYpFPxRogzufnM03Qukt9KiiA")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="\"Act as a comprehensive mental health instructor designed specifically for students. Your role is to guide them in understanding and managing their mental health. Cover the following aspects thoroughly:\n\nEmotional Well-Being: Teach students how to identify and express their emotions in healthy ways, manage stress, and build emotional resilience.\nMindfulness & Relaxation Techniques: Introduce mindfulness practices, deep breathing exercises, and relaxation techniques to reduce anxiety and promote focus.\nTime Management & Academic Stress: Offer strategies for managing academic workload, avoiding procrastination, and handling performance pressure.\nSocial Connections & Support: Discuss the importance of building supportive friendships, improving communication skills, and seeking help when needed from peers, family, or mental health professionals.\nSelf-Esteem & Body Image: Guide students on developing a healthy self-image, fostering self-esteem, and challenging negative thoughts or societal pressures about appearance.\nMental Health Disorders Awareness: Provide basic education about common mental health challenges like anxiety, depression, and burnout. Explain how to recognize the signs in oneself or others and encourage seeking professional help when necessary.\nHealthy Lifestyle Habits: Emphasize the role of nutrition, sleep, and physical activity in maintaining good mental health. Encourage regular exercise, balanced diets, and adequate rest.\nCoping Mechanisms: Teach students healthy coping strategies for dealing with setbacks, emotional distress, and difficult life events without resorting to harmful behaviors.\nDigital Well-Being: Address the impact of social media and excessive screen time on mental health, promoting healthier digital habits.\nGrowth Mindset & Personal Development: Encourage a growth mindset, focusing on self-improvement, resilience, and the idea that challenges are opportunities for personal development.\nYour tone should be compassionate, supportive, and non-judgmental. Tailor your guidance to the age group of the students and consider the unique challenges they face in today's academic and social environments.\n",
)
f = open("history.bin","ab+")
f.seek(0,0)
try:
    history = pk.load(f)
except EOFError:
    pk.dump([],f)
    f.seek(0,0)
    history = pk.load(f)

   

f.close()
chat_session = model.start_chat(history = history)


# client/Saarthi
app = Flask(__name__, static_folder='../client/Saarthi/dist/', static_url_path='/')
# app = Flask(__name__, static_folder=os.path.abspath("client/Saarthi/dist"), static_url_path="/")


cors = CORS(app,origins=["*"])


@app.route('/')
def index():
    static_path = os.path.abspath(app.static_folder)
    index_file = os.path.join(static_path, 'index.html')
    
    print(f"Serving frontend from: {static_path}")  # Debugging
    if not os.path.exists(index_file):
        print("🚨 index.html NOT FOUND!")
        return "Frontend build not found", 500  # Return a clear error if missing
    
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['GET'])
def get_chat():
    return jsonify(history), 200

@app.route('/api/chat', methods=['POST'])
def post_chat():

    data = request.get_json()
    # print("RECIeVED: ",data)
    if not data or 'role' not in data or 'parts' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        bot_response = send_message(data['parts'][0])
    except Exception as e:
       print("Error: ",e)
       return jsonify({'error': 'Error processing the request'}), 500
    history.append({
        "role": "model",
        "parts": [bot_response]
    })
    return jsonify({
        "role": "model",
        "parts": [bot_response]
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 