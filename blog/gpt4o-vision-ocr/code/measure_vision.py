import base64
import os
import time
import json

import requests
import tqdm

# OpenAI API Key
api_key = os.environ["API_KEY"]

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


pbar = tqdm.tqdm(total=110, unit="request")

for n in range(11):
    n *= 100
    dir_name = os.path.join("..", "result", "img", str(n))
    os.makedirs(dir_name, exist_ok=True)
    time_out = 60
    for i in range(10):
        # Path to your image
        image_path = os.path.join("..", "data", "img", str(n), str(i) + ".png")

        # Getting the base64 string
        base64_image = encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Count the amount of words in the image. Only respond with the total number, don't say anything else."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 10
        }

        start_time = time.perf_counter()
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        end_time = time.perf_counter()

        time_out -= (end_time - start_time) / 1000

        result = response.json()
        result["duration_ms"] = (end_time - start_time) * 1000

        with open(os.path.join(dir_name, str(i) + ".json"), "w") as file:
            json.dump(result, file)

        pbar.update(1)

    if time_out > 0:
        time.sleep(time_out)
