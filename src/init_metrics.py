import requests
import json

HOSTS = ["172.16.2.46", "172.16.1.133", "172.16.1.210", "172.16.1.211"]




def create_metrics():
    body = {
    "archive_policy_name": "high",
    }

    headers = {
        'Content-Type': 'application/json'
    }

    url = ''
    response = requests.post(url = url, data = body, headers = headers)
    resp_json = json.loads(response)
    return resp_json['id']

if __name__ == "__main__":
    id = []
    for i in range(len(HOSTS)):
        id[i] = create_metrics()
    print(id)