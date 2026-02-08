from openai import OpenAI

def print_hello_world():
    openai = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key = 'my-api-key',
    )

    response = openai.chat.completions.create(
        model="llama2:latest",
        messages=[{"role": "user", "content": "Write 'Hello, World!'"}],
    )

    print(response.choices[0].message.content)



if __name__ == "__main__":
    print_hello_world()
