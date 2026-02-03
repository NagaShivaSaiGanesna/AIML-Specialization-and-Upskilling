import requests
import json
import os
from datetime import datetime

# ----------------- API Configuration -----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3:mini"

CLAUDE_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

HISTORY_FILE = "chat_history.json"
SAVED_CONVOS_FILE = "saved_conversations.json"

MAX_HISTORY_LENGTH = 20
KEEP_RECENT_MESSAGES = 5

CURRENT_PROVIDER = "ollama"

# ----------------- Load or Create History -----------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("✅ Conversation history cleared!")
    else:
        print("ℹ️  No history to clear.")
    return []

# ----------------- Save Conversations -----------------
def load_saved_conversations():
    if os.path.exists(SAVED_CONVOS_FILE):
        with open(SAVED_CONVOS_FILE, "r") as f:
            return json.load(f)
    return []

def save_conversation(history, title=None):
    if not history:
        print("❌ No conversation to save (history is empty).")
        return
    
    if not title:
        title = input("Enter a title for this conversation: ").strip()
        if not title:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    saved = load_saved_conversations()
    saved.append({
        "title": title,
        "saved_at": str(datetime.now()),
        "messages": history.copy(),
        "provider": CURRENT_PROVIDER
    })
    
    with open(SAVED_CONVOS_FILE, "w") as f:
        json.dump(saved, f, indent=4)
    
    print(f"✅ Conversation saved as: '{title}'")

def list_saved_conversations():
    saved = load_saved_conversations()
    
    if not saved:
        print("📭 No saved conversations yet.")
        return
    
    print(f"\n{'='*60}")
    print(f"📚 Saved Conversations ({len(saved)} total)")
    print(f"{'='*60}")
    
    for i, convo in enumerate(saved, 1):
        provider = convo.get('provider', 'unknown')
        print(f"{i}. {convo['title']} [{provider}]")
        print(f"   Saved: {convo['saved_at']}")
        print(f"   Messages: {len(convo['messages'])}")
        print()

def view_saved_conversation():
    """View a specific saved conversation"""
    saved = load_saved_conversations()
    
    if not saved:
        print("📭 No saved conversations to view.")
        return
    
    list_saved_conversations()
    
    try:
        choice = int(input("Enter conversation number to view (0 to cancel): "))
        if choice == 0:
            return
        
        if 1 <= choice <= len(saved):
            convo = saved[choice - 1]
            print(f"\n{'='*60}")
            print(f"📖 {convo['title']}")
            print(f"{'='*60}\n")
            
            for msg in convo['messages']:
                print(f"You: {msg['user']}")
                print(f"AI: {msg['assistant']}")
                print()
        else:
            print("❌ Invalid conversation number.")
    except ValueError:
        print("❌ Invalid input.")

# ----------------- Summarization -----------------
def generate_summary(messages, system_msg):
    print("\n🔄 Generating summary...")
    
    convo_text = ""
    for msg in messages:
        convo_text += f"User: {msg['user']}\nAI: {msg['assistant']}\n\n"
    
    summary_prompt = f"""Provide a concise summary of this conversation:

{convo_text}

Summary:"""
    
    if CURRENT_PROVIDER == "ollama":
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": summary_prompt,
            "stream": False
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            data = response.json()
            return data.get("response", "Summary unavailable")
        except Exception as e:
            return f"Summary unavailable: {e}"
    
    elif CURRENT_PROVIDER == "claude":
        if not CLAUDE_API_KEY:
            return "Summary unavailable (no API key)"
        
        try:
            response = requests.post(
                CLAUDE_URL,
                headers={
                    "x-api-key": CLAUDE_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": CLAUDE_MODEL,
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": summary_prompt}]
                }
            )
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            return f"Summary unavailable: {e}"

def should_summarize(history):
    return len(history) > MAX_HISTORY_LENGTH

def summarize_history(history, system_msg):
    if not should_summarize(history):
        return history
    
    print(f"\n⚠️  History: {len(history)} messages (max: {MAX_HISTORY_LENGTH})")
    
    old_messages = history[:-KEEP_RECENT_MESSAGES]
    recent_messages = history[-KEEP_RECENT_MESSAGES:]
    
    summary = generate_summary(old_messages, system_msg)
    
    new_history = [
        {
            "user": "[Summary]",
            "assistant": summary,
            "time": str(datetime.now())
        }
    ] + recent_messages
    
    print(f"✅ Compressed: {len(history)} → {len(new_history)} messages\n")
    return new_history

# ----------------- Personas -----------------
PERSONAS = {
    "assistant": "You are a helpful AI assistant.",
    "coder": "You are an expert software engineer. Write clean and correct code.",
    "writer": "You are a creative writer. Use imaginative and expressive language.",
    "teacher": "You are a patient teacher. Explain concepts clearly with examples.",
    "analyst": "You are a data analyst. Provide structured, analytical responses."
}

def choose_persona():
    print("\n" + "="*60)
    print("Available Personas:")
    for i, (key, desc) in enumerate(PERSONAS.items(), 1):
        print(f"  {i}. {key.capitalize()}: {desc}")
    print("="*60)
    
    choice = input("Choose persona (1-5 or name): ").strip().lower()
    
    # Try number first
    try:
        num = int(choice)
        if 1 <= num <= len(PERSONAS):
            key = list(PERSONAS.keys())[num - 1]
            print(f"✅ Selected: {key.capitalize()}")
            return PERSONAS[key]
    except ValueError:
        pass
    
    # Try name
    if choice in PERSONAS:
        print(f"✅ Selected: {choice.capitalize()}")
        return PERSONAS[choice]
    
    # Default
    print("ℹ️  Defaulting to Assistant")
    return PERSONAS["assistant"]

# ----------------- AI Providers -----------------
def ask_ollama(prompt, system_msg, history):
    messages_text = system_msg + "\n\n"
    
    for m in history:
        messages_text += f"User: {m['user']}\n AI: {m['assistant']}\n"
    
    messages_text += f"User: {prompt}\nAI:"
    
    payload = {
        "model": OLLAMA_MODEL,
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
    
    print()
    return full_reply

def ask_claude(prompt, system_msg, history):
    if not CLAUDE_API_KEY:
        print("❌ ANTHROPIC_API_KEY not set!")
        return "Error: API key not configured"
    
    messages = []
    for m in history:
        messages.append({"role": "user", "content": m["user"]})
        messages.append({"role": "assistant", "content": m["assistant"]})
    
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 4096,
        "system": system_msg,
        "messages": messages,
        "stream": True
    }
    
    try:
        response = requests.post(
            CLAUDE_URL,
            headers={
                "x-api-key": CLAUDE_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json=payload,
            stream=True
        )
        
        full_reply = ""
        for line in response.iter_lines():
            if not line:
                continue
            
            line_text = line.decode("utf-8")
            if not line_text.startswith("data: "):
                continue
            
            data_str = line_text[6:]
            
            if data_str == "[DONE]":
                break
            
            try:
                data = json.loads(data_str)
                if data.get("type") == "content_block_delta":
                    chunk = data.get("delta", {}).get("text", "")
                    print(chunk, end="", flush=True)
                    full_reply += chunk
            except json.JSONDecodeError:
                continue
        
        print()
        return full_reply
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return f"Error: {e}"

def ask_ai(prompt, system_msg, history):
    if CURRENT_PROVIDER == "ollama":
        return ask_ollama(prompt, system_msg, history)
    elif CURRENT_PROVIDER == "claude":
        return ask_claude(prompt, system_msg, history)

def switch_provider():
    global CURRENT_PROVIDER
    
    print("\n" + "="*60)
    print("AI Providers:")
    print("  1. Ollama (local, free)")
    print("  2. Claude (Anthropic API, requires key)")
    print("="*60)
    
    choice = input("Select provider (1/2): ").strip()
    
    if choice == "1":
        CURRENT_PROVIDER = "ollama"
        print(f"✅ Switched to Ollama ({OLLAMA_MODEL})")
    elif choice == "2":
        if not CLAUDE_API_KEY:
            print("⚠️  ANTHROPIC_API_KEY not set!")
        CURRENT_PROVIDER = "claude"
        print(f"✅ Switched to Claude ({CLAUDE_MODEL})")
    else:
        print("❌ Invalid choice")

# ----------------- NEW: Main Menu System -----------------
def show_help():
    """Display comprehensive help menu"""
    print("\n" + "="*60)
    print("🤖 CHATBOT HELP MENU")
    print("="*60)
    print("\n📝 CHAT COMMANDS:")
    print("  /help      - Show this help menu")
    print("  /clear     - Clear conversation history")
    print("  /save      - Save current conversation")
    print("  /list      - List all saved conversations")
    print("  /view      - View a saved conversation")
    print("  /summarize - Summarize conversation now")
    print("  /stats     - Show conversation statistics")
    print("\n⚙️  SETTINGS:")
    print("  /persona   - Change AI persona")
    print("  /provider  - Switch AI provider (Ollama/Claude)")
    print("  /config    - Show current configuration")
    print("\n🚪 EXIT:")
    print("  exit       - Quit the chatbot")
    print("="*60 + "\n")

def show_stats(history):
    """Display conversation statistics"""
    if not history:
        print("📊 No statistics available (empty history)")
        return
    
    print("\n" + "="*60)
    print("📊 CONVERSATION STATISTICS")
    print("="*60)
    print(f"Total messages: {len(history)}")
    print(f"User messages: {len([m for m in history if 'user' in m])}")
    
    total_chars = sum(len(m.get('user', '')) + len(m.get('assistant', '')) for m in history)
    print(f"Total characters: {total_chars:,}")
    print(f"Average message length: {total_chars // max(len(history), 1)} chars")
    
    if history:
        first = history[0].get('time', 'Unknown')
        last = history[-1].get('time', 'Unknown')
        print(f"First message: {first}")
        print(f"Last message: {last}")
    
    print("="*60 + "\n")

def show_config():
    """Display current configuration"""
    print("\n" + "="*60)
    print("⚙️  CURRENT CONFIGURATION")
    print("="*60)
    print(f"Provider: {CURRENT_PROVIDER}")
    print(f"Model: {OLLAMA_MODEL if CURRENT_PROVIDER == 'ollama' else CLAUDE_MODEL}")
    print(f"Max history: {MAX_HISTORY_LENGTH} messages")
    print(f"Keep recent: {KEEP_RECENT_MESSAGES} messages")
    print(f"History file: {HISTORY_FILE}")
    print(f"Saved conversations: {SAVED_CONVOS_FILE}")
    
    saved = load_saved_conversations()
    print(f"Total saved: {len(saved)} conversations")
    
    if CURRENT_PROVIDER == "claude":
        api_status = "✅ Set" if CLAUDE_API_KEY else "❌ Not set"
        print(f"Claude API key: {api_status}")
    
    print("="*60 + "\n")

# ----------------- Main Loop with Menu -----------------
def main():
    global CURRENT_PROVIDER
    
    print("\n" + "="*60)
    print("🤖 ENHANCED AI CHATBOT")
    print("="*60)
    print("Type /help for commands")
    print("="*60 + "\n")
    
    history = load_history()
    system_msg = choose_persona()
    
    print(f"\n📡 Provider: {CURRENT_PROVIDER}")
    print("💬 Start chatting! (type 'exit' to quit)\n")
    
    while True:
        user_msg = input("You: ").strip()
        
        if not user_msg:
            continue
        
        # Exit command
        if user_msg.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        # Help command
        if user_msg.lower() == "/help":
            show_help()
            continue
        
        # Clear history
        if user_msg.lower() == "/clear":
            history = clear_history()
            continue
        
        # Save conversation
        if user_msg.lower() == "/save":
            save_conversation(history)
            continue
        
        # List saved conversations
        if user_msg.lower() == "/list":
            list_saved_conversations()
            continue
        
        # View saved conversation
        if user_msg.lower() == "/view":
            view_saved_conversation()
            continue
        
        # Force summarization
        if user_msg.lower() == "/summarize":
            if len(history) > KEEP_RECENT_MESSAGES:
                history = summarize_history(history, system_msg)
                save_history(history)
            else:
                print("ℹ️  Not enough messages to summarize.")
            continue
        
        # Show statistics
        if user_msg.lower() == "/stats":
            show_stats(history)
            continue
        
        # Change persona
        if user_msg.lower() == "/persona":
            system_msg = choose_persona()
            continue
        
        # Switch provider
        if user_msg.lower() == "/provider":
            switch_provider()
            continue
        
        # Show configuration
        if user_msg.lower() == "/config":
            show_config()
            continue
        
        # Regular chat message
        reply = ask_ai(user_msg, system_msg, history)
        
        history.append({
            "user": user_msg,
            "assistant": reply,
            "time": str(datetime.now()),
            "provider": CURRENT_PROVIDER
        })
        
        # Auto-summarize if needed
        if should_summarize(history):
            history = summarize_history(history, system_msg)
        
        save_history(history)

if __name__ == "__main__":
    main()