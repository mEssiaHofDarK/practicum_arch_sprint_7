import requests

data= {
    "question": "что такое кладда?",
}

resp = requests.post('http://127.0.0.1:8080/rag', data=data)

print(resp.json())
