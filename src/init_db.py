import json
from keystoneauth1 import session
from keystoneauth1.identity import v3

if __name__ == "__main__":
    
    GNOCCHI_URL = 'http://252.3.28.194:8041/v1/metric'

    # Retrieving hosts from json
    with open('./config_copy.json') as conf:
        config = json.load(conf)

    # Authentication
    auth = v3.Password(auth_url='http://252.3.28.251:5000/v3',
                       username='admin',
                       password='openstack',
                       project_id='a0ad9a8653254510b46538253032c380', 
                       user_domain_name='admin_domain')
    sess = session.Session(auth=auth)

    newconfig = {'hosts':[]}
    for host in config['hosts']:
        res = sess.post(url=GNOCCHI_URL, json={'archive_policy_name': 'medium', 'name': host['ip']}, headers={'Content-Type':'application/json'})
        data=json.loads(res.text)
        host['metric'] = data['id']
        newconfig['hosts'].append(host)

    with open("./config_copy.json", "w") as f:
        json.dump(newconfig, f)