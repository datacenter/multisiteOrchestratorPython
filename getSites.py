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


# first, let's list all users
resp = rc.get('/sites')
allSites = json.loads(resp.text)
for site in allSites['sites']:
    queryString = '/sites/' + site['id']
    siteInfo = rc.get(queryString)
    siteData = json.loads(siteInfo.text)
    siteName = siteData['name']
    print("Site {} [name {}] info".format(site['id'],siteName))
    print(80 * "=")
    pprint.pprint(siteData)


