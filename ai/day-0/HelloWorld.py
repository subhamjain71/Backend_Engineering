from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Tuple
import os

load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")

openai = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key = API_KEY
        )


def chat_with_llm(messages: List[dict], newPrompt: str, system: str='') -> Tuple[str, List[dict]]:
    """
    Chat with a llm with conversion history and a prompt.
    Args:
        messages (list): List of messages in the conversation history. Each message is a dict with 'role' and 'content'.
        prompt (str): The new prompt to send to the llm.
    Returns:
        (response_text, updated_messages)
    """
    if system:
        messages.append({"role": "system", "content": system})
    
    messages.append({"role": "user", "content": newPrompt})
    assistant_message = openai.chat.completions.create(
        model="llama2:latest",
        messages=messages,
    ).choices[0].message
    
    messages.append({"role": "assistant", "content": assistant_message.content})

    return assistant_message.content, messages



if __name__ == "__main__":
    print("🤖 Chat with Llama2 (type 'quit' to exit)\n")
    messages = [
        {"role": "system", "content": "You are a wise AI mentor teaching someone to become an AI engineer. Be encouraging but honest about the learning curve."}
    ]   
    while True:
        prompt = input("You: ")
        if prompt.lower() == "quit":
            print("Exiting chat. Goodbye!")
            break
        response, messages = chat_with_llm(messages, prompt)
        print(f"Assistant: {response}")
