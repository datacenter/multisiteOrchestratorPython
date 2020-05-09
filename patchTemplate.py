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
templateName = 'Template1'

# let's fetch the id of schema 'schema_one'
schemas = rc.get('/schemas')
schemasJson = json.loads(schemas.text)
for schema in schemasJson['schemas']:
    if schema['displayName'] == 'schema_one':
        schemaId = schema['id']
        siteId = schema['sites'][0]['siteId']

print("Schema has id {} and site is {}".format(schemaId,siteId))

path = '/sites/' + siteId + '-' + templateName + '/anps/ap_one/epgs/epg_one/staticPorts/-'

patchSet = [{ "op": "add",
             "path": path,
             "value": {
                            "type": "port",
                            "path": "topology/pod-1/paths-101/pathep-[eth1/17]",
                            "portEncapVlan": 51,
                            "deploymentImmediacy": "immediate",
                            "mode": "regular"
                          }
           }]

url = '/schemas/' + schemaId
resp = rc.patch(url, json_body=patchSet)
print("\n")
pprint.pprint(json.loads(resp.text))

