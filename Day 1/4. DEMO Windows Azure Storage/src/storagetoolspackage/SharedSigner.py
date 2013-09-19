from azure.storage import *
from azure.storage.sharedaccesssignature import *

from datetime import datetime, timedelta

class SharedSigner:


    def __init__(self, res_type, res_path, account_name, account_key):
        self.sas = SharedAccessSignature(account_name, account_key)
        self.sas.permission_set = [self._get_permission(res_type, res_path, 'r')]
        self.wr = self._get_signed_web_resource(res_type, res_path, "r")


    def _get_permission(self, resource_type, resource_path, permission):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        start = datetime.utcnow() - timedelta(minutes=1)
        expiry = start + timedelta(hours=1)

        sap = SharedAccessPolicy(AccessPolicy(start.strftime(date_format),
                                              expiry.strftime(date_format),
                                              permission))

        signed_query = self.sas.generate_signed_query_string(resource_path,
                                                        resource_type,
                                                        sap)

        return Permission('/' + resource_path, signed_query)

    def _get_signed_web_resource(self, resource_type, resource_path, permission):
        wr = WebResource()
        wr.properties[SIGNED_RESOURCE_TYPE] = resource_type
        wr.properties[SHARED_ACCESS_PERMISSION] = permission
        wr.path = '/' + resource_path
        wr.request_url = '/' + resource_path

        print(self.sas.permission_set)
        print(self.sas.account_key)

        return self.sas.sign_request(wr)
