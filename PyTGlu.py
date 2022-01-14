import requests
import json

'''
NEEDS COMMENTING
'''


class PyTglu():
    def __init__(self, api, url):
        self.api = api
        self.url = url
        self.get_request_headers = {"x-api-key": self.api,
                                    "Content-Type": "application/json"}
        self.post_request_headers = {"x-api-key": self.api,
                                     "Content-Type": "application/vnd.api+json"}

    def getGetRequestHeaders(self):
        return self.get_request_headers

    def getPostRequestHeaders(self):
        return self.post_request_headers

    def getUrl(self):
        return self.url


    def makeGetRequest(self, endpoint):
        c = requests.get(url=self.getUrl()+endpoint, headers=self.getGetRequestHeaders())
        return c

    def makePostRequest(self, endpoint, context):
        context = json.dumps(context)
        c = requests.post(url=self.getUrl() + endpoint, headers=self.getPostRequestHeaders(), data=context )
        return c

    def getResults(self, c):
        try:
            # request has been made
            c.raise_for_status()
        except:
            print(c.text)
            raise
        returned_data = c.json()
        return returned_data

    def getOrganisations(self):
        enpoint = 'organizations?page[size]=10000'
        c = self.makeGetRequest(enpoint)
        return self.getResults(c)

    def getConfigurationStatus(self):
        endpoint = 'configuration_statuses?page[size]=1000'
        return self.getResults(self.makeGetRequest(endpoint))

    def getOrganisation(self, org_id):
        enpoint = f'organizations/{org_id}'
        c = self.makeGetRequest(enpoint)
        return self.getResults(c)

    def getFlexibleAssetsForUnifi(self):
        enpoint = 'flexible_assets?filter[flexible-asset-type-id]=2263594763878652&page[size]=1000'
        c = self.makeGetRequest(enpoint)
        return self.getResults(c)

    def getFlexibleAssets(self, assetTypeId):
        enpoint = f'flexible_assets?filter[flexible-asset-type-id]={assetTypeId}'
        c = self.makeGetRequest(enpoint)
        return self.getResults(c)


    def getConfigurations(self, organisation_id):
        endpoint = f'organizations/{organisation_id}/relationships/configurations'
        c = self.makeGetRequest(endpoint)
        return self.getResults(c)

    def getConfigurationTypes(self):
        endpoint = f'configuration_types?page[size]=1000'
        c = self.makeGetRequest(endpoint)
        return self.getResults(c)

    def setConfigurations(self, organisation_id, context):
        endpoint = f'organizations/{organisation_id}/relationships/configurations'
        c = self.makePostRequest(endpoint, context)
        return self.getResults(c)

    def setManufacturers(self, context):
        endpoint = "manufacturers"
        c = self.makePostRequest(endpoint, context)
        return self.getResults(c)

    def getManufacturers(self):
        endpoint = 'manufacturers?page[size]=1000'
        c = self.makeGetRequest(endpoint)
        return self.getResults(c)

    def getContacts(self, organisation_id):
        endpoint = f"organizations/{organisation_id}/relationships/contacts"
        c = self.makeGetRequest(endpoint)
        return self.getResults(c)

    def getModels(self):
        endpoint = 'models?page[size]=1000'
        c = self.makeGetRequest(endpoint)
        return self.getResults(c)

    def buildConfigurationContext(self, name, installed_at,
                                 serial_number, mac, ip, organisation_id, config_type, contactId):
        context = {"data": {
            "type": "configurations",
            "attributes": {
                "name": name,
                "organisation_id": organisation_id,
                "manufacturer-id": '1539383725457621',
                "configuration-type-id": config_type,
                "primary_ip": ip,
                "mac_address": mac,
                "serial_number": serial_number,
                "installed_at": installed_at,
                "contact_id": contactId
                }
            }
        }
        return context

    def buildITGConfigurationContext(self, name, installed_at,
                                 serial_number, mac, ip, organisation_id, config_type, contactId, location_id):
        context = {"data": {
            "type": "configurations",
            "attributes": {
                "name": name,
                "organisation_id": organisation_id,
                "location_id": location_id,
                "manufacturer-id": '1539383725457621',
                "configuration-type-id": config_type,
                "configuration_status_id": "1539219934757003",
                "primary_ip": ip,
                "mac_address": mac,
                "serial_number": serial_number,
                "installed_at": installed_at,
                "contact_id": contactId
                }
            }
        }
        return context


    def upload_attachment(self, encoded_file, configuration_id, filename):
        endpoint = f'configurations/{configuration_id}/relationships/attachments'
        context = {
            "data": {
                "type": "attachments",
                "attributes": {
                    "attachment": {
                        "content": encoded_file,
                        "file_name": filename
                    }
                }
            }
        }
        c = self.makePostRequest(endpoint, context)
        return self.getResults(c)

    def getLocations(self, organisation_id):
        endpoint = f"organizations/{organisation_id}/relationships/locations"
        c = self.makeGetRequest(endpoint)
        return self.getResults(c)





