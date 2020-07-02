import requests
import json
import time
from prettytable import PrettyTable

aggregations = ["mean","min","max"]
granularity = [60,3600]
GNOCCHI_URL = 'http://252.3.28.194:8041/v1/metric/{0}/measures?aggregation={1}&granularity={2}&' 

def get_request(token, metric, aggr_type , granularity):
    """
        Read the data from gnocchi db.
        ------------
        params:
            token: openstack authentication token
            metric: metric id
            aggr_type: type of aggregation [mean, min, max]
            granularity: granularity of the aggregation [60, 3600]
    """
    header = {} 
    header['X-AUTH-TOKEN'] = token
    return requests.get(url=GNOCCHI_URL.format(metric,aggr_type,granularity), headers = header).json()

    
if __name__ == "__main__":
    print("Please, chose a type of aggregation:\n")
    aggregation_type = int(input("1) Mean\n2) Min\n3) Max\n"))
    print("Please, chose a granularity:\n")
    gran = int(input("1) Minute\n2) Hour\n"))

    # retrieving token and hosts from json
    with open('./config.json') as conf:
        config = json.load(conf)

    while True:
        for host in config['hosts']:
            res = get_request(config['token'], host['metric'], aggregations[aggregation_type-1], granularity[gran-1])
            print('\033[1m' + "Host: " + host['ip'] + '\033[0m')
            for i in res:
                t = PrettyTable(['Timestamp', 'Granularity', aggregations[aggregation_type-1].upper()])
                t.add_row([i[0], i[1], i[2]])
            print(t)
        time.sleep(30)