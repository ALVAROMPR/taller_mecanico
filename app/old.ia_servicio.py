import requests
import json

API_KEY = "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"

def analizar_ventas(data):
    prompt = f"Analiza los datos de ventas y proporciona un resumen de las tendencias y patrones. Datos: {data}"
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }),
        timeout=10
    )
    result = response.json()
    print(result)
    return result["choices"][0]["message"]["content"]