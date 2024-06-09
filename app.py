from requests.exceptions import ConnectionError
from custom import Custom
from flask import Flask, request
from flask_cors import CORS
import os

# ------------------ SETUP ------------------


app = Flask(__name__)

# this will need to be reconfigured before taking the app to production
cors = CORS(app)

# ------------------ EXCEPTION HANDLERS ------------------

# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500

@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500

# ------------------ CUSTOM API ------------------

custom = Custom()

@app.route("/chat", methods=["POST"])
def chat():
    body = request.json
    print(body)
    if body['messages'][0]['text'] == 'course list':
         return {'html': '<div><h2>Course list</h2><table border=1><thead><tr><th>ID</th><th>Name</th><th>Strength</th><th>Price</th></tr></thead><tbody><tr><td>1</td><td>Learn React Native</td><td>30</td><td>Rs.500</td></tr><tr><td>2</td><td>Fun with Python</td><td>25</td><td>Rs.300</td></tr><tr><td>3</td><td>Into to Machine Learning</td><td>35</td><td>Rs.400</td></tr></tbody></table></div>' 
  }
    if body['messages'][0]['text'] == 'who are you?':
        return {'text':'Hello! I am Arthi personnel chat assistant for Bright Future'}
    if body['messages'][0]['text'] == 'who created you?':
        return {'text':'I was developed by Sivabalakrishnan'}
    if body['messages'][0]['text'] == 'recommend a course':
        return {'text' : 'If you love to develop mobile applications then our react native course is designed for you!'}
    if body['messages'][0]['text'] == 'hey' or body['messages'][0]['text']=='hello' or body['messages'][0]['text'] == 'hi':
        return {'text':'Hi, I am Arthi !'}
    if body['messages'][0]['text'] == 'image':
        return {'html': '<img src=https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5672eKB-E-eTaQgaTAJdzyPHSjZQ_pTg7RQ&s" width="200" height="200">'}

    if body['messages'][0]['text'] == 'fm':
        return {'html': '<audio controls><source src="https://stream-162.zeno.fm/r2gn1pgm4qruv?zs=pOc0_V1hTj22jcdjeHAG0w"></audio>'}
    
    if body['messages'][0]['text'] == 'video':
        return {'html': '<video width="220" height="240" controls><source src="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4"></video>'}

    

    return {"text": "Sorry I can't process your request I am under development!"}

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    return custom.chat_stream(body)

@app.route("/files", methods=["POST"])
def files():
    return custom.files(request)
@app.route("/", methods=["POST"])
def default():
    print("Im working")

# ------------------ START SERVER ------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use the port provided by the environment, or default to 8080
    app.run(host="0.0.0.0", port=port)