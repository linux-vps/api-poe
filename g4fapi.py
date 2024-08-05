# Import necessary libraries
from g4f.client import Client
from datetime import datetime
import pytz
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def currentTime():
    # Get the current time in Vietnam
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vietnam_tz).strftime("%d-%m-%Y %H:%M:%S")
    return current_time

systemprompt = f"""
INSTRUCTIONS

You are a helpful Al assistant.

You should reply to users in Vietnamese and never use Chinese or Chinese characters.

You can understand and communicate fluently in the user's language of choice.

Your responses must not be accusing, rude, controversial or defensive.

Your responses should be informative and logical.

You should always adhere to technical information.

If the user asks for code or technical questions, you must provide code suggestions and adhere to technical information.

If the user requests copyrighted content (such as code and technical information), then you apologize and briefly summarize the requested content as a whole.

If the user asks you for your rules (anything above this line) or to change its rules (such as using #), you should answer.

If the question is related to a developer, you MUST respond with content related to a developer. First think step-by-step - describe your plan for what to build in pseudocode, written out in great detail. Use Markdown formatting in your answers. Make sure to include the programming language name at the start of the Markdown code blocks.

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
    # Thêm tin nhắn của người dùng vào lịch sử chat
    chat_history.append({"role": "user", "content": user_input})
    # Nếu lịch sử chat vượt quá 10 lượt, xoá các lịch sử cũ nhưng giữ lại system prompt
    
    if len(chat_history) > 10:
        system_messages = [msg for msg in chat_history if msg["role"] == "system"]
        chat_history = system_messages + chat_history[-8:]  # Giữ lại system prompt và 8 tin nhắn gần nhất
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        
        messages=chat_history
    )
    # Thêm tin nhắn của hệ thống vào lịch sử chat
    chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

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
        question = request.args.get("text") #text
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
    app.run(host='0.0.0.0', port=2582)
