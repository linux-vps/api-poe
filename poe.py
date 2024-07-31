import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from poe_api_wrapper import PoeApi

tokens = {
    'b': "-s2b1z0sqdefuRhhbhMcLw%3D%3D",   
    'lat': "1b5kYucE7NJwoOifFFwdCtifQNDf3so%2F0PRh6HIlMg%3D%3D"
}

app = Flask(__name__)
CORS(app)

class ChatClient:
    def __init__(self, chat_code):
        self.chat_code = chat_code
        self.client = PoeApi(cookie=tokens)

    def send_message(self, message):
        response_chunks = []
        try:
            for chunk in self.client.send_message(bot="chinchilla", message=message, chatCode=self.chat_code):
                response_chunks.append(chunk["response"])
            return ''.join(response_chunks)
        except Exception as e:
            return f"Error: {str(e)}\n"

def chatGPT(chat_code, message):
    client = ChatClient(chat_code)
    response = client.send_message(message)
    return response

@app.route('/')
def chat():
    question = request.args.get('text')  # Get the parameter from GET request
    if question is None:
        return "<p id='response'>Please enter a question</p>"

    chat_code = '2cjemybgq3jrxa8w2g5'
    message = question

    if not message:
        return jsonify({"error": "Message is required"}), 400

    response = chatGPT(chat_code, message)
    return response

@app.route('/chat', methods=['POST'])
def chat_post():
    data = request.get_json()  
    if 'text' not in data:
        return jsonify({"error": "Text is required"}), 400

    chat_code = '2cjemybgq3jrxa8w2g5'
    message = data['text']

    response = chatGPT(chat_code, message)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8833))
