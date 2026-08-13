import requests
url = "https://api.example.com/users/1"
payload = {"name": "test"} 
r = requests.get(url, timeout=5)
r = requests.post(url, json={"name": "test"}, headers={"Authorization": "Bearer x"})
r = requests.put(url, data=payload)
r = requests.delete(url)

r.status_code        # 200
r.json()             # parsed body
r.text               # raw body
r.headers
r.elapsed            # response time - useful for performance assertions
r.ok                 # True if status < 400
r.raise_for_status() # raises HTTPError on 4xx/5xx