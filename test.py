import requests

base_url = "http://127.0.0.1:5000/"
text = "New Text"

response = requests.put(base_url + f"message", data={"message": text})
print(response.json())
input()
response = requests.get(base_url + f"message")
print(response.json())