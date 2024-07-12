import json
import os
import time

import requests
import tqdm

# OpenAI API Key
api_key = os.environ["API_KEY"]

pbar = tqdm.tqdm(total=110, unit="request")

for n in range(11):
    n *= 100
    dir_name = os.path.join("..", "result", "txt", str(n))
    os.makedirs(dir_name, exist_ok=True)
    time_out = 60
    for i in range(10):
        txt_path = os.path.join("..", "data", "txt", str(n), str(i) + ".txt")

        with open(txt_path, "r") as file:
            text = file.read()

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
                            "text": "Count the amount of words in the following text, only respond with the total number, don't say anything else:\n\n```" + text + "```"
                        }
                    ]
                }
            ],
            "max_tokens": 10
        }

        start_time = time.perf_counter()
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        end_time = time.perf_counter()

        time_out -= end_time - start_time

        result = response.json()
        result["duration_ms"] = (end_time - start_time) * 1000

        with open(os.path.join(dir_name, str(i) + ".json"), "w") as file:
            json.dump(result, file)

        pbar.update(1)

    if time_out > 0:
        time.sleep(time_out)
