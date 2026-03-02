import json
import os
import subprocess
from datetime import datetime

from flask import Flask, request
from markdown import markdown
from markupsafe import escape
from . import chatting
from .misc import style, greeting

app = Flask(__name__)

def git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

def get_user() -> str:
    return os.environ.get('BARAMIND_USER', 'default')

def chat_file_name() -> str:
    return f"chats/{datetime.now().date().isoformat()}-{git_revision_short_hash()}-{get_user()}.json"

def save_chat(chat):
    with open(chat_file_name(), "w") as f:
        json.dump(chat, f, indent=2)

def load_chat():
    try:
        with open(chat_file_name()) as f:
            return json.load(f)
    except FileNotFoundError:
        save_chat([])
        with open(chat_file_name()) as f:
            return json.load(f)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/sample_tool_call_response")
def sample_tool_call_response():
    response = chatting.sample_tool_calling_chat()
    return f"<html><body>{response}</body></html>"


@app.route("/chatui", methods=["GET", "POST"])
def chat_ui():
    chat_so_far = load_chat()
    if request.method == "POST":
        if "new_message" not in request.form:
            raise ValueError()
        new_user_message = request.form.get("new_message").strip()
        chat_so_far.append({"role": "user", "content": new_user_message})
        new_bot_message = chatting.sample_tool_calling_chat(chat_input=chat_so_far[:15])
        chat_so_far.append({"role": "assistant", "content": new_bot_message})
        save_chat(chat_so_far)
    # We're assuming user input needs escaping and bot input doesn't. Which is a dangerous assumption,
    # but we likely won't be doing this in our real use case anyway.
    interleaved_html_messages = []
    for obj in chat_so_far:
        if obj["role"] == "user":
            interleaved_html_messages.append(f"""      <div class="message user">{escape(obj["content"])}</div>""")
        else:
            converted = markdown(obj["content"], extensions=['extra', 'nl2br', 'sane_lists'])
            interleaved_html_messages.append(f"""      <div class="message bot">{converted}</div>""")
    # put an anchor on latest message to make it easy to scroll to the bottom via javascript on load
    if interleaved_html_messages:
        interleaved_html_messages[-1] = interleaved_html_messages[-1].replace("div", "div id=\"latest\"")
    interleaved_html_messages_str = "\n".join(interleaved_html_messages)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Chat UI</title>
  <style>
    {style}
  </style>
</head>
<script>
  document.addEventListener("DOMContentLoaded", (event) => {{
      if (!(!!window.location.hash)) {{
        window.location.href = window.location.href + "#latest";
      }}
    }});
</script>
<body>
 <form action="" method="POST">
  <div class="chat-container">
    <div class="messages">
      <div class="message bot">{greeting}</div>
      {interleaved_html_messages_str}
    </div>
    <div class="input-bar">
      <input type="text" name="new_message" placeholder="Type a message..." />
      <button>Send</button>
    </div>
  </div>
 </form>
</body>
</html>
    """
