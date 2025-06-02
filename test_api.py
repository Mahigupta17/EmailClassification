import requests

url = "https://<your-username>-<space-name>.hf.space/classify"  # Replace with your real URL
data = {
    "input_email_body": "Subject: Assistance Request\nMy name is John Doe. You can reach me at john@example.com"
}

res = requests.post(url, json=data)
print(res.json())
