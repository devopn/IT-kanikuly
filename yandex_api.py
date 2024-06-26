from datetime import datetime
import httpx
import json
import base64
import asyncio
from config import config
yandex_cloud_catalog = config.yandex_cloud_catalog
yandex_api_key = config.yandex_api_key
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
async def get_image(prompt, temperature, sys_promt, seed) -> bytes:
    print(sys_promt)
    body = {
    "modelUri": f"art://{yandex_cloud_catalog}/yandex-art/latest",
    "generationOptions": {"seed": seed, "temperature": temperature},
    "messages": [
        {"weight": 1, "text": sys_promt}
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
        {"role": "user", "text": prompt},
    ],
    }
    if system_prompt:
        body["messages"].update({"role": "system", "text": system_prompt})

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
        done = response_json["done"]
        while not done:
            response = await client.get(url, headers=headers)
            response_json = json.loads(response.text)
            done = response_json["done"]
            await asyncio.sleep(0.5)
            
    answer = response_json["response"]["alternatives"][0]["message"]["text"]
    return answer

    
async def geocode(address: str) -> dict:
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {"apikey": apikey, "geocode": address, "format": "json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    # response = httpx.get(url, params=params)
    response_json = json.loads(response.text)
    features = response_json["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]["boundedBy"]["Envelope"]

