import json
import time
from prettytable import PrettyTable
from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneauth1 import exceptions


aggregations = ["mean","min","max"]
granularity = [60,3600]
GNOCCHI_URL = 'http://252.3.28.194:8041/v1/metric/{0}/measures?aggregation={1}&granularity={2}&' 

if __name__ == "__main__":
    print("Please, chose a type of aggregation:\n")
    aggregation_type = int(input("1) Mean\n2) Min\n3) Max\n"))
    print("Please, chose a granularity:\n")
    gran = int(input("1) Minute\n2) Hour\n"))

    # retrieving hosts from json
    with open('./config.json') as conf:
        config = json.load(conf)

    auth = v3.Password(auth_url='http://252.3.28.251:5000/v3',  #OS_AUTH_URL, si trovano nel admin-openrc.sh
                       username='admin', #OS_USERNAME
                       password='openstack',
                       project_id='a0ad9a8653254510b46538253032c380',  #OS_PROJECT_ID, 
                       user_domain_name='admin_domain')  #OS_USER_DOMAIN_NAME

    sess = session.Session(auth=auth)

    while True:
        for host in config['hosts']:
            res = sess.get(url=GNOCCHI_URL.format(host['metric'], aggregations[aggregation_type-1], granularity[gran-1]))
            data=json.loads(res.text)   
            print('\033[1m' + "Host: " + host['ip'] + '\033[0m')
            print(str(data))
            t = PrettyTable(['Timestamp', 'Granularity', aggregations[aggregation_type-1].upper()])

            for i in data[(0 if len(data)<5 else len(data)-5):len(data)]:   #stampa i 5 piu recenti
                t.add_row([i[0], i[1], i[2]])

            print(t)
        time.sleep(30)
