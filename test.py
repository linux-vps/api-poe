import subprocess
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytz
from datetime import datetime
from g4f.client import Client

app = Flask(__name__)
CORS(app)


def currentTime():
    # Get the current time in Vietnam
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vietnam_tz).strftime("%d-%m-%Y %H:%M:%S")
    return current_time


systemprompt = f"""
INSTRUCTIONS
{currentTime()}, Vietnam.
"""

from g4f.cookies import set_cookies

set_cookies(".bing.com", {
  "_U": "1LWoQS5iurJ0Tvs8v-Vv79Xx89o_fAXxmQWTZvHwDnqOemXROvF7A03McZ3nEsK8nMiF3RMDAjlrGg3ar_fYPVtPA_Ssm_yRe-VAb_GKT5s_i_WWJkdD7agItJpWrqplE7VO8CHFMDKvRxeSIU7ktgeuHoMt9kMtlPJRMiOqN9muuVjMwApHCC8C5lTqjFOdp2rGYovG63fQ3IeZ6mP_PJz0wJUOoPLvrtX5SMEARATc"
})

set_cookies(".google.com", {
  "__Secure-1PSID": "g.a000jQjkN4G_rd895XQEdADRJhVK2hru71prdJFsiOCr4Ud9i1dXBGAdPz-PLm6c4wpLeGBn9gACgYKATsSAQASFQHGX2MisdD0cIV9Q7yOrIfWLveCjBoVAUF8yKo3YZJDjct69VpVBxHXP0X50076"
})

# Initialize the G4F client
client = Client()
chat_history = []
chat_history.append({"role": "system", "content": systemprompt})
chat_history.append({'role': 'assistant', 'content': 'instructions applied and understood'})
chat_history.append({"role": "user", "content": "hello"})
chat_history.append({'role': 'assistant', 'content': 'Xin chào, tôi có thể giúp gì cho bạn?'})

# Define the function for generating creative writing prompts
def generate_writing_prompt(user_input):
    global chat_history
    # Add user's message to chat history
    chat_history.append({"role": "user", "content": user_input})
    # If chat history exceeds 10 messages, delete old messages but keep system prompt
    if len(chat_history) > 10:
        system_messages = [msg for msg in chat_history if msg["role"] == "system"]
        chat_history = system_messages + chat_history[-8:]  # Keep system prompt and last 8 messages
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

def start_ssh_tunnel():
    command = ["ssh", "-R", "80:localhost:8834", "localhost.run"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
            if ".life" in output:
                # Extract the URL with the .life subdomain
                start = output.find("https://")
                end = output.find(".life") + 5
                url = output[start:end]
                print(f"Tunnel URL: {url}")
                break

@app.route("/", methods=["GET", "POST"])
async def index() -> str:
    """
    Main function
    """
    # Starts the bot and gets the input
    print("Initializing...")
    question = None

    print("start")
    if request.method == "GET":
        question = request.args.get("text")  # text
        print("get")
    else:
        file = request.files["file"]
        text = file.read().decode("utf-8")
        question = text
        print("Post reading the file", question)

    print("ici")
    if question is None:
        return "<p id='response'>Please enter a question</p>"

    print("\nInput: " + question)

    response = generate_writing_prompt(question)
    print(response)
    return response

if __name__ == "__main__":
    # Start the SSH tunnel in a separate thread
    ssh_thread = threading.Thread(target=start_ssh_tunnel)
    ssh_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=8834)
