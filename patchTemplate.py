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
schemaName = 'schema_one'

# let's fetch the id of schema 'schema_one'
schemas = rc.get('/schemas')
schemasJson = json.loads(schemas.text)
for schema in schemasJson['schemas']:
    if schema['displayName'] == schemaName:
        schemaId = schema['id']
        # for sake of simplicity we are retrieving the first site only
        siteId = schema['sites'][0]['siteId']

print("Schema has id {} and site is {}".format(schemaId, siteId))

# let's add three static paths to an EPG in Template1
path = '/sites/' + siteId + '-' + templateName + \
    '/anps/ap_one/epgs/epg_one/staticPorts/-'

baseVlan = 50
baseInterface = 17
pathCount = 5
patchSet = []

for i in range(pathCount):
    print(i)
    pathPath = 'topology/pod-1/paths-101/pathep-[eth1/%s]' % str(
        baseInterface+i)
    pathVlan = baseVlan+i
    pathItem = {"op": "add",
                "path": path,
                "value": {
                    "type": "port",
                    "path": pathPath,
                    "portEncapVlan": pathVlan,
                    "deploymentImmediacy": "immediate",
                    "mode": "regular"
                }
                }
    patchSet.append(pathItem)

url = '/schemas/' + schemaId
resp = rc.patch(url, json_body=patchSet)
print("\n")
pprint.pprint(json.loads(resp.text))
delOp = input(
    "Check MSO for new static path under EPG. Delete paths now? [Y/N]")
if delOp == 'Y':
    path = '/sites/' + siteId + '-' + templateName + \
        '/anps/ap_one/epgs/epg_one/staticPorts/'
    patchSet = [{"op": "remove",
                 "path": path,
                 "value": {}
                 }]
    resp = rc.patch(url, json_body=patchSet)
    print("Paths removed")
