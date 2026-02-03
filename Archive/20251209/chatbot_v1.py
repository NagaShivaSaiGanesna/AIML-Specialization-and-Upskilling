#!/usr/bin/env python3
# chatbot_v1.py (Updated: Adds HuggingFace Local mode)

import json
import subprocess
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# -------------------------------------------------------
# Load Persona
# -------------------------------------------------------
def get_persona(option):
    if option == "1":
        return "You are an AI assistant. Be helpful and friendly."
    elif option == "2":
        return "You are an expert coder. Provide highly optimized code."
    elif option == "3":
        return "You are a skilled writer. Produce clean and engaging text."
    return "You are an AI assistant."

# -------------------------------------------------------
# Ollama (Local)
# -------------------------------------------------------
def ask_ollama(prompt, system_msg, history):
    messages = []
    if system_msg:
        messages.append({"role": "system", "content": system_msg})
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": prompt})

    process = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    input_data = json.dumps({"messages": messages})
    out, err = process.communicate(input_data)
    return out.strip()

# -------------------------------------------------------
# Claude API (Anthropic)
# -------------------------------------------------------
def ask_claude(prompt, system_msg, history):
    import requests
    import os

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "ERROR: Missing ANTHROPIC_API_KEY"

    messages = []
    if system_msg:
        messages.append({"role": "system", "content": system_msg})
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 3000,
        "messages": messages,
    }

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json=body,
    )

    data = r.json()
    if "content" not in data:
        return f"API ERROR: {data}"

    return data["content"][0]["text"]

# -------------------------------------------------------
# HuggingFace LOCAL MODE
# -------------------------------------------------------
TOKENIZER = None
MODEL = None

# Load local HF model once

def load_hf_model():
    global TOKENIZER, MODEL

    if TOKENIZER is None:
        print("Loading HuggingFace model (local)...")
        TOKENIZER = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
        MODEL = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.1",
            torch_dtype=torch.float16,
            device_map="auto",
        )


def ask_huggingface_local(prompt, system_msg, history):
    load_hf_model()

    full_prompt = system_msg + "\n\n"
    for u, a in history:
        full_prompt += f"User: {u}\nAssistant: {a}\n"
    full_prompt += f"User: {prompt}\nAssistant:"

    inputs = TOKENIZER(full_prompt, return_tensors="pt").to(MODEL.device)
    output = MODEL.generate(
        **inputs,
        max_new_tokens=400,
        do_sample=True,
        temperature=0.7,
    )

    reply = TOKENIZER.decode(output[0], skip_special_tokens=True)
    if "Assistant:" in reply:
        reply = reply.split("Assistant:")[-1].strip()
    return reply

# -------------------------------------------------------
# Main Chat Loop
# -------------------------------------------------------
def main():
    print("\nChoose persona:")
    print("1. Assistant")
    print("2. Coder")
    print("3. Writer")
    persona = input("\nEnter option (1/2/3): ")
    system_msg = get_persona(persona)

    print("\nSelect Mode:")
    print("1. Use Ollama (Local)")
    print("2. Use Claude (Anthropic API)")
    print("3. Use HuggingFace (LOCAL Model)")
    mode = input("\nEnter option (1/2/3): ")

    print("\nChat started! Type 'exit' to quit.")
    print("Commands: /clear, /save, /mode\n")

    history = []

    while True:
        user_msg = input("You: ")

        if user_msg.lower() == "exit":
            break
        if user_msg.lower() == "/clear":
            history = []
            print("Chat history cleared.\n")
            continue

        if mode == "1":
            reply = ask_ollama(user_msg, system_msg, history)
        elif mode == "2":
            reply = ask_claude(user_msg, system_msg, history)
        else:
            reply = ask_huggingface_local(user_msg, system_msg, history)

        print(f"\nAssistant: {reply}\n")
        history.append((user_msg, reply))


if __name__ == "__main__":
    main()
