import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Unifier():
    '''
    Caller to a unifi controller. The caller has a variety of functions, the most useful of which is likely
    make_request. simply add your endpoint as an argument, for example 'api/self/sites' and it will give you the data
    returned by the call.

    I am in the process of building smaller, more specific functions that take no arguments and print the results out
    in a readable way. As i discover more enpoints i will make more direct functions.

    TODO: error handling

    Author: Patrick Ward

    Date: 10/12/2020

    '''
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.headers  = {"Accept": "application/json",
                   "Content-Type": "application/json"}

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_headers(self):
        return self.headers

    def make_request(self, endpoint):
        '''
        makes a request to your controller taking the endpoint as an argument
        :param endpoint: the endpoint of the url you are calling with the api call. eg/ 'api/self/sites'
        :return: an unprocessed dictionary containing the data returned by the caller
        '''
        # Set credentials and URL for the API call

        host = self.get_host()
        port = self.get_port()
        url = f"https://{host}:{port}/api/login"
        user = self.get_user()
        password = self.get_password()
        headers = self.get_headers()

        # Set the headers and body for the call

        body = {
            'username': user,
            'password': password,
        }

        # Create a session object
        session = requests.Session()

        # Use the session object to make the call to the API
        response = session.post(url, headers=headers,
                                data=json.dumps(body), verify=False, )

        # Open the Json object returned by the call
        response = response.json()


        # If you are logged in
        if response['meta']['rc'] == 'ok':
            endpoint = endpoint
            url = f"https://{host}:{port}/{endpoint}"
            response = session.get(url, headers=headers, verify=False,)
            response = response.json()
            response = response['data']

            return response

        else:
            print('Login failed, please check your credentials')



    def make_post_request(self, endpoint, context):
        '''
        makes a request to your controller taking the endpoint as an argument
        :param endpoint: the endpoint of the url you are calling with the api call. eg/ 'api/self/sites'
        :return: an unprocessed dictionary containing the data returned by the caller
        '''
        # Set credentials and URL for the API call

        host = self.get_host()
        port = self.get_port()
        url = f"https://{host}:{port}/api/login"
        user = self.get_user()
        password = self.get_password()
        headers = self.get_headers()

        # Set the headers and body for the call

        body = {
            'username': user,
            'password': password,
        }

        # Create a session object
        session = requests.Session()

        # Use the session object to make the call to the API
        response = session.post(url, headers=headers,
                                data=json.dumps(body), verify=False, )

        # Open the Json object returned by the call
        response = response.json()

        # If you are logged in
        if response['meta']['rc'] == 'ok':
            endpoint = endpoint
            url = f"https://{host}:{port}/{endpoint}"
            response = session.post(url, headers=headers, verify=False, data=json.dumps(context))
            response = response.json()
            #response = response['data']
            return response

        else:
            print('Login failed, please check your credentials')


    def make_put_request(self, endpoint, context):
        '''
        makes a request to your controller taking the endpoint as an argument
        :param endpoint: the endpoint of the url you are calling with the api call. eg/ 'api/self/sites'
        :return: an unprocessed dictionary containing the data returned by the caller
        '''
        # Set credentials and URL for the API call

        host = self.get_host()
        port = self.get_port()
        url = f"https://{host}:{port}/api/login"
        user = self.get_user()
        password = self.get_password()
        headers = self.get_headers()

        # Set the headers and body for the call

        body = {
            'username': user,
            'password': password,
        }

        # Create a session object
        session = requests.Session()

        # Use the session object to make the call to the API
        response = session.post(url, headers=headers,
                                data=json.dumps(body), verify=False, )

        # Open the Json object returned by the call
        response = response.json()
        print(response)

        # If you are logged in
        if response['meta']['rc'] == 'ok':
            endpoint = endpoint
            url = f"https://{host}:{port}/{endpoint}"
            response = session.put(url, headers=headers, verify=False, data=json.dumps(context))
            response = response.json()
            print(response)
            #response = response['data']
            return response

        else:
            print('Login failed, please check your credentials')

    def get_sites(self):
        return self.make_request('api/self/sites')

    def get_devices(self, site_id):
        endpoint = f'api/s/{site_id}/stat/device'
        return self.make_request(endpoint=endpoint)

    def get_device_basics(self, site_id):
        endpoint = f'api/s/{site_id}/stat/device-basic'
        return self.make_request(endpoint=endpoint)

    def check_site_health(self, site_id):
        endpoint = f'api/s/{site_id}/stat/health'
        return self.make_request(endpoint=endpoint)

    def get_site_alarms(self, site_id):
        endpoint = f'api/s/{site_id}/stat/alarm'
        return self.make_request(endpoint=endpoint)

    def get_site_events(self, site_id):
        endpoint = f'api/s{site_id}stat/event'
        return self.make_request(endpoint=endpoint)
