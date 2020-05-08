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
pprint.pprint(json.loads(resp.text))
