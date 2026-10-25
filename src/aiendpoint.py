import json
import os
from openai import OpenAI
import requests
#HCAPI





def req(full_prompt,mime_type,b64img,endpoint,api_key,model):
    
    client = OpenAI(
        base_url = endpoint,
        api_key = api_key
    )


    completion = client.chat.completions.create(
        model=model,
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