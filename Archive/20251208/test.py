import requests
import json
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"

HISTORY_FILE = r'C:\Users\ShivaGanesna\Downloads\IGTMUAD\20251208\chat_history.json'


# ----------------- Load or Create History -----------------

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        print((f))
        print('Hello')
return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# ----------------- Persona System Prompts -----------------
PERSONAS = {
    "assistant": "You are a helpful AI assistant.",
    "coder": "You are an expert software engineer. Write clean and correct code.",
    "writer": "You are a creative writer. Use imaginative and expressive language."
}


def choose_persona():
    print("Choose persona: assistant / coder / writer")
    p = input("Enter persona: ").strip().lower()

    if p not in PERSONAS:
        p = "assistant"

    return PERSONAS[p]


# ----------------- Chat Function -----------------
def ask_ollama(prompt, system_msg, history):
    """Send prompt to Ollama using /api/generate with streaming."""
    messages_text = system_msg + "\n\n"

    for m in history:
        messages_text += f"User: {m['user']}\n AI: {m['assistant']}\n"

    messages_text += f"User: {prompt}\nAI:"

    payload = {
        "model": MODEL_NAME,
        "prompt": messages_text,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    full_reply = ""
    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))
        chunk = data.get("response", "")
        print(chunk, end="", flush=True)
        full_reply += chunk

    print()  # newline
    return full_reply


# ----------------- Main Loop -----------------
def main():
    history = load_history()
    system_msg = choose_persona()

    print("\nChat started! Type 'exit' to quit.\n")

    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() == "exit":
            print("Goodbye!")
            break

        reply = ask_ollama(user_msg, system_msg, history)

        history.append({
            "user": user_msg,
            "assistant": reply,
            "time": str(datetime.now())
        })
        save_history(history)


if __name__ == "__main__":
    main()
