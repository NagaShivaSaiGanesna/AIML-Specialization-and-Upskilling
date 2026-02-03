import tiktoken  # OpenAI's tokenizer library

# Initialize tokenizer for your model
def get_tokenizer(model_name):
    """Get appropriate tokenizer"""
    # For OpenAI models
    if "gpt" in model_name:
        return tiktoken.encoding_for_model(model_name)
    # For other models, use approximate counter
    return tiktoken.get_encoding("cl100k_base")

def count_tokens(text, tokenizer):
    """Count tokens in text"""
    return len(tokenizer.encode(text))

def estimate_cost(input_tokens, output_tokens, model="gpt-4"):
    """Estimate API cost"""
    # Pricing per 1000 tokens
    prices = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "claude-sonnet": {"input": 0.003, "output": 0.015},
    }
    
    if model not in prices:
        return 0.0
    
    input_cost = (input_tokens / 1000) * prices[model]["input"]
    output_cost = (output_tokens / 1000) * prices[model]["output"]
    
    return input_cost + output_cost

# Modified ask_ollama function
def ask_ollama(prompt, system_msg, history):
    """Send prompt with token counting"""
    
    # Build full context
    messages_text = system_msg + "\n\n"
    for m in history:
        messages_text += f"User: {m['user']}\n AI: {m['assistant']}\n"
    messages_text += f"User: {prompt}\nAI:"
    
    # COUNT INPUT TOKENS
    tokenizer = get_tokenizer(MODEL_NAME)
    input_tokens = count_tokens(messages_text, tokenizer)
    
    print(f"📊 Input tokens: {input_tokens}")
    
    # Send request
    payload = {
        "model": MODEL_NAME,
        "prompt": messages_text,
        "stream": True
    }
    response = requests.post(OLLAMA_URL, json=payload, stream=True)
    
    # Stream response
    full_reply = ""
    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode("utf-8"))
        chunk = data.get("response", "")
        print(chunk, end="", flush=True)
        full_reply += chunk
    
    # COUNT OUTPUT TOKENS
    output_tokens = count_tokens(full_reply, tokenizer)
    
    print()  # newline
    print(f"📊 Output tokens: {output_tokens}")
    print(f"📊 Total tokens: {input_tokens + output_tokens}")
    
    # ESTIMATE COST (if using paid API)
    cost = estimate_cost(input_tokens, output_tokens, MODEL_NAME)
    print(f"💰 Estimated cost: ${cost:.4f}")
    
    return full_reply, input_tokens, output_tokens
'''

## **What This Shows You:**

### **Example Output:**

You: Explain quantum computing in simple terms

📊 Input tokens: 245
Hello! Quantum computing is... [response streams here]
📊 Output tokens: 387
📊 Total tokens: 632
💰 Estimated cost: $0.0189

'''