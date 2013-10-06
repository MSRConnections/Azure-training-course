from azure import *
from azure.servicemanagement import *

import credentials

class StorageManager:

    # create the service management client
    def __init__(self, storage_account_name):
        self.sm = ServiceManagementService(credentials.subscriptionid, credentials.certificate)
        self.storage_account_name = storage_account_name
        self.storage_account_key = None

    # creates a storage account with the prescribed name
    def CreateStorage(self):
        # this blows up - in the tests it looks like it's used to get the details and returns without incident
        # tests need updating because this always returns a 404 if it doesn't exist
        props = None
        try:
            props = self.sm.get_storage_account_properties(self.storage_account_name)
            print 'Storage account ' + self.storage_account_name + ' exists already'
        except WindowsAzureMissingResourceError:
            if props is None:
                self.sm.create_storage_account(self.storage_account_name, description = 'Created by MSR-Courseware', label = 'msrcourseware', affinity_group=None, location='North Europe', geo_replication_enabled=True, extended_properties=None)
                print 'Creating storage account ' + self.storage_account_name + ' in North Europe'


    # deletes a storage account with the prescribed name
    def DeleteStorage(self):
        self.sm.delete_storage_account(self.storage_account_name)
        print 'Deleting storage account ' + self.storage_account_name

    # displays the account details with keys
    def GetAccountCredentials(self):
        keys = self.sm.get_storage_account_keys(self.storage_account_name)
        print 'Getting storage keys for account ' + self.storage_account_name
        print 'primary key is ' + keys.storage_service_keys.primary
        print 'secondary key is ' + keys.storage_service_keys.secondary
        self.storage_account_key = keys.storage_service_keys.primary
        return self.storage_account_key




