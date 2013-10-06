__author__ = 'azurecoder'

from azure.servicebus import *
import base64
import Constants

class MsrServiceBusQueueClient:
    def __init__(self, servicebus_namespace = Constants.servicebus_namespace, servicebus_issuer = Constants.servicebus_issuer, servicebus_key = Constants.servicebus_key):
        self.servicebus_namespace = servicebus_namespace
        self.servicebus_issuer = servicebus_issuer
        self.servicebus_key = servicebus_key
        self.servicebus_service = ServiceBusService(service_namespace=servicebus_namespace, account_key=servicebus_key,issuer=servicebus_issuer)
        # take the MSR payload here which will contain the GPS info and supplementary info
        if self.servicebus_service.create_queue('msrdevices'):
            print 'Queue created called msrdevices'
        else:
            print 'Queue msrdevices already exists'

    def SendQueueMessage(self, payload):
        msg = Message(payload.GetJSONObject())
        self.servicebus_service.put_message('msrdevices',msg)
        print 'Sending message payload ' + payload.GetJSONObject()
