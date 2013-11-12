#The file will send a new task to a sample NCBI BLAST Windows Azure Cloud Service (http://blast2.cloudapp.net/)
#It is a sample file for "Azure 4 Research" Training.


#import libraries
from azure.servicebus import *
from azure.storage import *
import uuid
import random
import time
import json

#define service namespace, account key and issuer
#we have already defined it for you
servicenamespace = 'blast2-ns'
accountkey = 'XpHbdRgNEEodWLiKct7Nc6PrXKn9TGN6KYOIFHygxZw='
issuer = 'owner'
queue_name='JobQueue'

#create bus_service
bus_service = ServiceBusService(service_namespace=servicenamespace, account_key=accountkey, issuer=issuer)

#create a new message
msg = Message()

id = str(uuid.uuid1()).replace('-','')
input_file = 'input_' + str(random.randint(1,200))
last_timestamp = int(time.time()*10000) + 621355968000000000
name = 'TEST ' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '(' + input_file + ')'
data = {'Hash':"",
         'Id':id,
         'InputFile': input_file,
         'InputFiles':"null",
         'LastMessage':"Queued",
         'LastTimestamp': last_timestamp,
         'Name': name,
         'OutputFile':"",
         'State':"QUEUED"
         }

s=json.dumps(data);
msg.body=json.dumps(data);

print msg.body

#insert the message to table first
account = 'blaststore'
key = '99serQiW4MXGx4u14SfZTiONYDZ5jn7BRgOcRsQEcY/WCgzJxWwoSCXSTmPQnXwoUJkrQPgDjrzIr5AO9q71/Q=='
table_name = 'SearchTask'
table_service = TableService(account_name=account, account_key=key)

entity = Entity()
entity.PartitionKey = data['Id']
entity.RowKey= data['Id']
entity.Id = data['Id']
entity.Name = data['Name']
entity.InputFile = data['InputFile']
entity.State = data['State']
entity.LastMessage = data['LastMessage']
entity.LastTimestamp = data['LastTimestamp']
table_service.insert_entity(table_name, entity)

#submit the message to service bus queue
bus_service.send_queue_message(queue_name, msg)

#receive a new message
msgrec = bus_service.receive_queue_message(queue_name, False)
print msgrec.body 


#receive a new message when peek lock = True
msgrec = bus_service.receive_queue_message(queue_name, True)
print msgrec.body 
