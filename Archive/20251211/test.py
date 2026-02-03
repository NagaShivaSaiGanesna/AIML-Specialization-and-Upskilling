import tiktoken  # OpenAI's tokenizer library

# Initialize tokenizer for your model
def get_tokenizer(model_name="gpt-4o-mini"):
    """Get appropriate tokenizer"""
    try:
        return tiktoken.encoding_for_model(model_name)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")

def count_tokens(text, model_name="gpt-4o-mini"):
    tokenizer = get_tokenizer(model_name)
    return len(tokenizer.encode(text))

print(count_tokens('Hiii'))

