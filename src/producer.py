import time
import paramiko
import requests 
import json
from datetime import datetime

GNOCCHI_URL = 'http://252.3.28.194:8041/v1/metric/{0}/measures'

def get_memory_info(host):
    """
        Perform a ssh request to the host, 
        perform the "free -m" command 3 times (one each 4 seconds) 
        and get the memory usage percentage.
        -------
        params:
            host: {"hostname":hostname, "user":user, "password":password}
    """
    print("Open connection to: {0}".format(host['ip']))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host['ip'],username=host['user'],password=host['password'])
    
    result = []
    num_request = 0
    while num_request < 3:
        print("Getting memory data {req: d}".format(req=num_request+1), end="\r", flush=True)
        stdin, stdout, stderr = ssh_client.exec_command('free -m')
        memory_usage = stdout.read().decode("utf-8").split()
        timestamp = str(datetime.now().replace(microsecond=0))
        result.append({"timestamp" : timestamp,"value" : round(int(memory_usage[8])/int(memory_usage[7]) * 100, 2)})
        num_request += 1
        time.sleep(4)
    print("Data retreived, closing connection")
    ssh_client.close()
    return result


def post_request(url, token, values):
    """
        Push the data to gnocchi db.
        ------------
        params:
            body: post body data
    """
    print("Sending data to gnocchi")
    header = {}
    header['Content-Type'] = 'application/json'
    header['X-AUTH-TOKEN'] = token
    response = requests.post(url = url, json=values, headers=header) 
    code_resp = response.status_code
    print("Response status: " + str(code_resp))
    

if __name__ == "__main__":
    # retrieving token and hosts from json
    with open('./config.json') as conf:
        config = json.load(conf)

    while True:
        for host in config['hosts']:
            body = get_memory_info(host)   
            post_request(GNOCCHI_URL.format(host['metric']),config['token'], body)
            print("Data:")
            for value in body:
                print("Timestamp: {0} Memory Usage: {1} %".format(value['timestamp'], value['value']))
        time.sleep(30)