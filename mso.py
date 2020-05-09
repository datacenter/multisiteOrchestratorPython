#
# Minimal MSO SDK v1.0
#
# cpaggen May 2020
#

import requests
import warnings
import sys
import json

class RestClient(object):
    """
    A class for communicating with the MSO REST API using any of the SUPPORTED_METHODS below.
    
    Attributes:
        server_endpoint: string of API URL to query
        uri_prefix: string prefix of URI path
        admin_user: string of admin user
        admin_password: string of admin password
        verify: boolean for SSL verification of requests

    Constants:
        SUPPORTED_METHODS: list of supported HTTP methods
    """

    SUPPORTED_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def __init__(self, server_endpoint, admin_user, admin_password, **kwargs):
        """
        Init gets a bearer auth token first. That is required to interact with the API.
        In this version, login domains are not implemented. Local auth only for now.
        The bearer is then used when building HTTP requests for any of the SUPPORTED_METHODS.

        Example:
        rc = RestClient("my-mso.example.org", # https is always prefixed
                        "admin",              # api user
                        "cisco123",           # api user password
                        verify = False)       # disable SSL certification verification


        Args:
            server_endpoint: string of the server URL to query
            admin_user:      string of admin user
            admin_password:  string of admin password
            kwargs:
                api_version: API Version
                verify:      boolean to verify SSL cerfications
        """
        self.server_endpoint = server_endpoint
        self.uri_prefix = '/api/' + kwargs.get('api_version', 'v1')
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.verify = kwargs.get('verify', False)
        self.session = requests.Session()
        self.protocol = 'https'
        self.bearer = self.__login(server_endpoint, admin_user, admin_password)

    def __login(self, server_endpoint, admin_user, admin_password):
        # __login is called by __init__ only
        loggedIn = self.__msoLogMeIn(server_endpoint, admin_user, admin_password)
        if loggedIn:
            return loggedIn
        else:
            print("Failed to log in. Please verify credentials.")
            sys.exit(2)
       

    def make_http_request(self, http_method, uri_path, args=None):
        """
        Send an http request to the server. Returns a requests.Response.

        Args:
            http_method: String HTTP method like 'GET', 'PUT', 'POST', ...
            uri_path: Additional string URI path for query
            args: Additional dictionary of arguments
                "params": Additional dictionary of parameters for GET and PUT
                "json_body": String JSON body

        Returns:
            requests.Response object for the request
        """
        if http_method not in self.SUPPORTED_METHODS:
            warnings.warn('HTTP method "%s" is unsupported. Returning None' %
                          http_method)
            return None

        args = {} if args is None else args
        params = args.get('params')
        auth_header = {   'Authorization' : 'Bearer ' + self.bearer, \
                          'Accept': 'application/json'   }
        json_body = args.get('json_body', '')
        unprep_req = requests.Request(
            http_method, self.protocol + '://' + self.server_endpoint + uri_path, params=params,
            json=json_body, headers=auth_header)
        req = self.session.prepare_request(unprep_req)
        return self.session.send(req, verify=self.verify)

    def __msoLogMeIn(self, ip_addr, username, password):
        url = self.protocol + '://' + ip_addr + '/api/v1/auth/login'
        json_creds = '{"username" : "%s", "password" : "%s"}' % (username, password)
        mso_headers = {   'Host': ip_addr, \
                          'Origin': 'https://'+ip_addr, \
                          'Content-Type': 'application/json;charset=UTF-8', \
                          'Accept-Language': 'en-US,en;q=0.8,fr;q=0.6,nl;q=0.4', \
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/61.0.3163.100 Safari/537.36', \
                          'Referer': 'https://'+ip_addr, \
                          'Accept':'*/*'}
 
        req = requests.post(url, data=json_creds, verify=False, headers=mso_headers)
        
        if req.status_code == 201:
            retval = json.loads(req.text)
            return(retval['token'])
        else:
            return None

    def get(self, uri_path='', **kwargs):
        """
        GET request to the server. Returns a requests.Response.

        Args:
            uri_path: string URI path for query
            kwargs:
                params: additional dictionary of parameters for GET
                json_body: string JSON body

        Returns:
            requests.Response object for the request
        """
        return self.make_http_request(
            http_method='GET', uri_path=self.uri_prefix + uri_path, args=kwargs)

    def patch(self, uri_path='', **kwargs):
        """
        PATCH request to the server. Returns a requests.Response.

        Args:
            uri_path: string URI path for query
            kwargs:
                params: additional dictionary of parameters for PATCH
                json_body: string JSON body

        Returns:
            requests.Response object for the request
        """
        return self.make_http_request(
            http_method='PATCH', uri_path=self.uri_prefix + uri_path, args=kwargs)
    
    def delete(self, uri_path='', **kwargs):
        """
        DELETE request to the server. Returns a requests.Response.

        Args:
            uri_path: string URI path for query
            kwargs:
                params: additional dictionary of parameters for DELETE
                json_body: string JSON body

        Returns:
            requests.Response object for the request
        """
        return self.make_http_request(
            http_method='DELETE', uri_path=self.uri_prefix + uri_path, args=kwargs)

    def post(self, uri_path='', **kwargs):
        """
        POST request to the server. Returns a requests.Response.

        Args:
            uri_path: string URI path for query
            kwargs:
                params: additional dictionary of parameters for POST
                json_body: string JSON body

        Returns:
            requests.Response object for the request
        """
        return self.make_http_request(
            http_method='POST', uri_path=self.uri_prefix + uri_path,
            args=kwargs)

    def put(self, uri_path='', **kwargs):
        """"
        PUT request to the server. Returns a requests.Response.

        Args:
            uri_path: string URI path for query
            kwargs:
                params: additional dictionary of parameters for PUT
                json_body: string JSON body
        Returns:
            requests.Response object for the request
        """
        return self.make_http_request(
            http_method='PUT', uri_path=self.uri_prefix + uri_path,
            args=kwargs)

