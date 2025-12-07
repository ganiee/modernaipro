import requests
import json
import time

class OllamaChat:
    def __init__(self, base_url="http://localhost:11434", model="deepseek-r1:1.5b"):
        self.base_url = base_url
        self.model = model
        self.history = []
        self.temperature = 0.7
        
    def get_available_models(self):
        """Get list of available models from Ollama server"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return [model["name"] for model in response.json().get("models", [])]
            else:
                print(f"Error: Server returned status code {response.status_code}")
                return []
        except Exception as e:
            print(f"Error connecting to Ollama server: {e}")
            return []
    
    def send_message(self, message):
        """Send a message to the Ollama API and get the response"""
        # Add user message to history
        self.history.append({"role": "user", "content": message})
        
        # Prepare request data
        data = {
            "model": self.model,
            "messages": self.history,
            "options": {
                "temperature": self.temperature
            }
        }
        
        try:
            # Make the API request
            response = requests.post(
                f"{self.base_url}/api/chat",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data)
            )
            
            if response.status_code != 200:
                print(f"Error: Server returned status code {response.status_code}")
                print(response.text)
                return None
            
            # Process the response
            response_data = response.json()
            assistant_message = response_data.get('message', {}).get('content', '')
            
            # Add assistant response to history
            if assistant_message:
                self.history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            print(f"Error communicating with Ollama API: {e}")
            return None
    
    def change_model(self, model_name):
        """Change the model being used"""
        self.model = model_name
        print(f"Changed model to {model_name}")
        
    def reset_conversation(self):
        """Reset the conversation history"""
        self.history = []
        print("Conversation history reset")


def main():
    # Initialize the chat client
    chat = OllamaChat()
    
    print("Welcome to Ollama Chat!")
    print(f"Connected to {chat.base_url}")
    
    # Check available models
    print("Checking available models...")
    models = chat.get_available_models()
    if models:
        print(f"Available models: {', '.join(models)}")
        model_choice = input(f"Choose a model (default is {chat.model}): ")
        if model_choice.strip() and model_choice in models:
            chat.change_model(model_choice)
    else:
        print("Couldn't retrieve models. Make sure Ollama is running.")
    
    print(f"Chatting with {chat.model}")
    print("Type ':quit' to exit, ':reset' to reset conversation, or ':model NAME' to change model")
    
    # Main chat loop
    while True:
        user_input = input("\n> ")
        
        # Handle commands
        if user_input.lower() == ":quit":
            break
        elif user_input.lower() == ":reset":
            chat.reset_conversation()
            continue
        elif user_input.lower().startswith(":model "):
            model_name = user_input[7:].strip()
            chat.change_model(model_name)
            continue
        
        # Send message and get response
        print("\nThinking...", end="", flush=True)
        response = chat.send_message(user_input)
        print("\r" + " " * 10 + "\r", end="")  # Clear "Thinking..." text
        
        if response:
            print(f"\n{response}")
        else:
            print("\nNo response received. Check server connection.")

if __name__ == "__main__":
    main()