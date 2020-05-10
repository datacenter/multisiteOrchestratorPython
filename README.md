# A simple Python REST client class for ACI MSO (Multisite Orchestrator)

Using this code you can easily interact with MSO's REST API.

## How-to

Just populate **credentials.py** with your MSO's IP address, username and password.
Import mso.py in your code and instantiate a REST client like so:

```
try:
    from credentials import MSO_IP, MSO_ADMIN, MSO_PASSWORD
except ImportError:
    sys.exit("Error: please verify credentials file format.")

rc = mso.RestClient(MSO_IP, MSO_ADMIN, MSO_PASSWORD)
```

Once that's created, you can invoke supported HTTP verbs (GET, POST, PUT, PATCH, DELETE) like so:

```
resp = rc.get('/sites')
allSites = json.loads(resp.text)
```

Take a look at the examples provided for further assistance.
