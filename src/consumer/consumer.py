import requests
import json

def get_request(host):
    url = ''
    response = requests.get(url=url)
    resp_json = json.loads(response)

    
if __name__ == "__main__":
    time_span = ''
    granularity = ''

    hostname = "172.16.2.46"
    avg = get_request(hostname)