import ollama

def ask(prompt,mime_type,b64_data):
    res = ollama.chat(
        model="qwen3.5:4b",
        messages=[
            {
                'role':"User",
                'content':prompt,
                'images':[b64_data]
            }
        ]
    )
    print(res['message']['content'])
    return res['message']['content']