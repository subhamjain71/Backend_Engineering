from openai import OpenAI
from typing import List, Dict
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Create OpenAI client configured for Ollama
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key=os.getenv("OPEN_AI_KEY", "ollama")
)

def query_model(model: str, prompt: str, system: str = "") -> Dict:
    """
    Send a prompt to a specific model and measure response time.
    
    Args:
        model: Name of the Ollama model (e.g., "llama3.2", "qwen2.5:7b")
        prompt: User's question/prompt
        system: Optional system message to set behavior
    
    Returns:
        Dict with model name, response, and timing info
    """
    messages = []
    
    if system:
        messages.append({"role": "system", "content": system})
    
    messages.append({"role": "user", "content": prompt})
    
    # Start timer
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        
        # Calculate elapsed time
        elapsed = time.time() - start_time
        
        return {
            "model": model,
            "response": response.choices[0].message.content,
            "time_seconds": round(elapsed, 2),
            "success": True
        }
    
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "model": model,
            "response": f"ERROR: {str(e)}",
            "time_seconds": round(elapsed, 2),
            "success": False
        }


def compare_models(prompt: str, models: List[str], system: str = ""):
    """
    Compare how different models respond to the same prompt.
    
    Args:
        prompt: The question/prompt to test
        models: List of model names to compare
        system: Optional system message for all models
    """
    print(f"\n{'='*80}")
    print(f"PROMPT: {prompt}")
    if system:
        print(f"SYSTEM: {system}")
    print('='*80)
    
    results = []
    
    for model in models:
        print(f"\n🔄 Querying {model}...")
        result = query_model(model, prompt, system)
        results.append(result)
        
        if result["success"]:
            print(f"✅ {model} responded in {result['time_seconds']}s")
        else:
            print(f"❌ {model} failed")
    
    # Display results
    print(f"\n{'='*80}")
    print("RESULTS")
    print('='*80)
    
    for result in results:
        print(f"\n--- {result['model'].upper()} ({result['time_seconds']}s) ---")
        if result["success"]:
            print(result['response'])
        else:
            print(f"ERROR: {result['response']}")
        print("-" * 80)
    
    # Show timing comparison
    print("\n⏱️  SPEED COMPARISON:")
    sorted_results = sorted(results, key=lambda x: x['time_seconds'])
    for i, result in enumerate(sorted_results, 1):
        status = "✅" if result["success"] else "❌"
        print(f"  {i}. {result['model']}: {result['time_seconds']}s {status}")


if __name__ == "__main__":
    # Define models to compare
    models_to_test = [
        "llama3.2",
        "qwen2.5:7b",
        "mistral",
        "phi3"
    ]
    
    # Test 1: Simple factual question
    print("\n" + "🧪 TEST 1: FACTUAL QUESTION" + "\n")
    compare_models(
        prompt="Explain what a token is in LLMs in exactly 2 sentences.",
        models=models_to_test
    )
    
    # Test 2: Creative task
    print("\n\n" + "🧪 TEST 2: CREATIVE WRITING" + "\n")
    compare_models(
        prompt="Write a creative opening line for a sci-fi story about AI.",
        models=models_to_test
    )
    
    # Test 3: Structured output
    print("\n\n" + "🧪 TEST 3: STRUCTURED OUTPUT" + "\n")
    compare_models(
        prompt="List 3 benefits of local LLMs vs cloud APIs. Format as: 1. [benefit] 2. [benefit] 3. [benefit]",
        models=models_to_test
    )
