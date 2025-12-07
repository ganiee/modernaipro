# 1. Do a pip install of langchain: pip install langchain-groq
# 2. In an .env file setup GROQ_API_KEY=gsk-tqwgtqwt
import time
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

# Model names
models = {
    "deepseek-r1-distill-llama-70b": "Deepseek R1 Distill Llama 70b",
    "llama-3.1-8b-instant": "Llama3.1 8b Instant",
    "gemma2-9b-it": "Gemma 2 9b IT",
    "qwen-2.5-32b": "Qwen 2.5 32b"
}

# Test each model
for model_name, model_display_name in models.items():
    llm = ChatGroq(model_name=model_name)

    start_time = time.time()
    response = llm.invoke(
        "Talk about your most favorite EPL football club in 2 sentences")
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Output the results
    print(f"Model: {model_display_name}")
    print(f"Response: {response}")
    print(f"API call latency: {elapsed_time:.3f} seconds\n")
