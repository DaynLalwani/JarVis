import json
import os
from openai import OpenAI
import requests
#HCAPI
#OEPNROUTER.AI  - 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
def print_all_models():
    URL = "http://n1.eclipsesystems.org:30012/v1/models"


    headers = {
        "Authorization": f"Bearer sk-561d9f586320cb2fa9dc3ab374375152abf459bf2a65946a"
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    print(data)




def req(full_prompt,mime_type,b64img):
    #Write and ask api key
    try:
        with open("C:\\ProgramData\\KILOAI_API_KEY.txt", "x", encoding="utf-8") as file:
            apikey = input("Enter your GROQ api key : ")
            file.write(apikey)
            file.close()
    except FileExistsError:
        pass
    with open("C:\\ProgramData\\KILOAI_API_KEY.txt","r+",encoding="utf-8") as apk:
        content = apk.read()
        apikey = content
        client = OpenAI(
            base_url = "https://openrouter.ai/api/v1",
            api_key = "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"
            )


    completion = client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
                max_tokens=200, 
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": full_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{b64img}"
                                }
                            }
                        ]
                    }
                ]
            )

    return completion.choices[0].message.content