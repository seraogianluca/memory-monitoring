import json
from keystoneauth1 import session
from keystoneauth1.identity import v3

if __name__ == "__main__":
    
    GNOCCHI_URL = 'http://**PLACE_YOUR_GNOCCHI_IP_HERE**/v1/metric'

    # Retrieving hosts from json
    with open('./config.json') as conf:
        config = json.load(conf)

    # Authentication
    auth = v3.Password(auth_url='http://**PLACE_YOUR_KEYSTONE_IP_HERE**/v3',
                       username='**OPENSTACK_USERNAME**',
                       password='**OPENSTACK_PASSWORD**',
                       project_id='**OPENSTACK_PROJECT_ID**', 
                       user_domain_name='**OPENSTACK_USER_DOMAIN**')
    sess = session.Session(auth=auth)

    newconfig = {'hosts':[]}
    for host in config['hosts']:
        res = sess.post(url=GNOCCHI_URL, json={'archive_policy_name': 'medium', 'name': host['ip']}, headers={'Content-Type':'application/json'})
        data=json.loads(res.text)
        host['metric'] = data['id']
        newconfig['hosts'].append(host)

    with open("./config.json", "w") as f:
        json.dump(newconfig, f)
