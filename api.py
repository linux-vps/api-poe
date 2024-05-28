import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from poe_api_wrapper import PoeApi

tokens = {
    'b': "-s2b1z0sqdefuRhhbhMcLw%3D%3D",
    'lat': "KjhgTCfSmIYEXieP6VXtECuKkX0GAMkaaDC%2B2l61wA%3D%3D"
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
            for chunk in self.client.send_message(bot="gpt3_5", message=message, chatCode=self.chat_code):
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

    chat_code = '2c77oexhhct8s6gvgr0'
    message = question

    if not message:
        return jsonify({"error": "Message is required"}), 400

    response = chatGPT(chat_code, message)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8000))
