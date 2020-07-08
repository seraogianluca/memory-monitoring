import time
import paramiko
import json
from datetime import datetime
from keystoneauth1 import session
from keystoneauth1.identity import v3


GNOCCHI_URL = 'http://**GNOCCHI_IP**/v1/metric/{0}/measures'

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
        stdin, stdout, stderr = ssh_client.exec_command('free -m')
        memory_usage = stdout.read().decode("utf-8").split()
        timestamp = str(datetime.now().replace(microsecond=0))
        result.append({"timestamp" : timestamp,"value" : round(float(memory_usage[8])/float(memory_usage[7]) * 100, 2)})
        num_request += 1
        time.sleep(4)
    print("Data retreived, closing connection")
    ssh_client.close()
    return result

if __name__ == "__main__":
    # Retrieving hosts from json
    with open('/root/config.json') as conf:
        config = json.load(conf)

    # Authentication
    auth = v3.Password(auth_url='http://**OPENSTACK_IP**/v3',
                       username='**OPENSTACK_USER**',
                       password='**OPENSTACK_PASSWORD**',
                       project_id='**OPENSTACK_PROJECT_ID**', 
                       user_domain_name='**OPENSTACK_USER_DOMAIN**')
    sess = session.Session(auth=auth)

    while True:
        for host in config['hosts']:
            body = get_memory_info(host) 
            print("Sending data to gnocchi")
            res = sess.post(url=GNOCCHI_URL.format(host['metric']), json=body, headers={'Content-Type':'application/json'})
            print("Response status: " + str(res))
            print("Data:")
            for value in body:
                print("Timestamp: {0} Memory usage: {1} %".format(value['timestamp'], value['value']))
        time.sleep(30)
