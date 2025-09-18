import requests

data= {
    "question": "кто такая миреска?",
}

resp = requests.post('http://127.0.0.1:8080/rag', data=data)

print(resp.json())
