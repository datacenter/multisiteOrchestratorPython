import json
import sys
import mso
import urllib3
import json
import pprint

try:
    from credentials import MSO_IP, MSO_ADMIN, MSO_PASSWORD
except ImportError:
    sys.exit("Error: please verify credentials file format.")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
rc = mso.RestClient(MSO_IP, MSO_ADMIN, MSO_PASSWORD)

roles = rc.get('/roles')
rolesJson = json.loads(roles.text)
for role in rolesJson['roles']:
    if role['name'] == 'powerUser':
        roleId = role['id']

userJson = {"lastName":"Testing",
            "username":"test",
            "phoneNumber":"555-123-456",
            "emailAddress":"test@example.org",
            "id":"",
            "firstName":"Subject",
            "confirmPassword":"cisco123!!!!",
            "password":"cisco123!!!!",
            "roles":[ {"roleId":roleId,
                       "accessType":"readOnly"}],
            "accountStatus":"active"}

resp = rc.post('/users', json_body=userJson)
respJson = json.loads(resp.text)
newUserId = respJson['id']
print("Created new user with id {}".format(newUserId))
discard = input("Take a look at MSO for the presence of the new user. Should we delete it? [Y/N] ")
if discard == "Y":
    path = '/users/' + newUserId
    resp = rc.delete(path)
    if resp.status_code == 204:
        print("User deleted")
