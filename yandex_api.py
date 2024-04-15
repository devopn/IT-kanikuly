from datetime import datetime
import httpx
import json
import base64
import asyncio
from config import config
yandex_cloud_catalog = config.yandex_cloud_catalog
yandex_api_key = config.yandex_api_key

async def get_image(prompt, temperature) -> bytes:
    seed = int(round(datetime.now().timestamp()))

    body = {
    "modelUri": f"art://{yandex_cloud_catalog}/yandex-art/latest",
    "generationOptions": {"seed": seed, "temperature": temperature},
    "messages": [
        {"weight": 1, "text": prompt[:499]},
    ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {"Authorization": f"Api-Key {yandex_api_key}"}

    response = httpx.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    operation_id = response_json["id"]

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {yandex_api_key}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response_json = json.loads(response.text)
        done = response_json["done"]
        while not done:
            await asyncio.sleep(1)
            response = await client.get(url, headers=headers)
            response_json = json.loads(response.text)
            done = response_json["done"]

    image_data = response_json["response"]["image"]
    return base64.b64decode(image_data)


async def get_text(prompt, temperature, limit=400, system_prompt="") -> str:
    yandex_gpt_model = "yandexgpt-lite"
    body = {
    "modelUri": f"gpt://{yandex_cloud_catalog}/{yandex_gpt_model}",
    "completionOptions": {"stream": False, "temperature": temperature, "maxTokens": limit},
    "messages": [
        {"role": "system", "text": system_prompt},
        {"role": "user", "text": prompt},
    ],
}

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": yandex_cloud_catalog,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        
    response_json = json.loads(response.text)
    operation_id = response_json["id"]
    url = f"https://llm.api.cloud.yandex.net/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {yandex_api_key}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response_json = json.loads(response.text)
        # print(response_json)
        done = response_json["done"]
        while not done:
            response = await client.get(url, headers=headers)
            response_json = json.loads(response.text)
            done = response_json["done"]
            # print(response_json)
            await asyncio.sleep(0.5)
            
    answer = response_json["response"]["alternatives"][0]["message"]["text"]
    return answer

    