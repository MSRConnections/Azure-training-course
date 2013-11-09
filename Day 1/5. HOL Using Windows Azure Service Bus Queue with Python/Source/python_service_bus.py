# The file will send a new task to a sample NCBI BLAST Windows Azure Cloud Service (http://azure4research-blast.cloudapp.net/)
# It is a sample file for "Azure 4 Research" Training.


# Import libraries
from azure.servicebus import *
from azure.storage import *
import uuid
import random
import time
import json

# Define service namespace, account key and issuer (we have already defined it for you :))
servicenamespace = 'sb-azure4research-blast'
accountkey = 'aC7HfbvW8t7+851wyCEI8DinXg2KTS1voDb2yqyUZZ8='
issuer = 'owner'
queue_name='JobQueue'

# Define a connection to our Service Bus Namespace
bus_service = ServiceBusService(service_namespace=servicenamespace, account_key=accountkey, issuer=issuer)

# Create a new message
msg = Message()

id = str(uuid.uuid1()).replace('-','')
input_file = 'input_' + str(random.randint(1,200))
last_timestamp = int(time.time()*10000) + 621355968000000000
name = 'TEST ' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '(' + input_file + ')'
data = { 'Hash': "",
         'Id': id,
         'InputFile': input_file,
         'InputFiles': "null",
         'LastMessage': "Queued",
         'LastTimestamp': last_timestamp,
         'Name': name,
         'OutputFile': "",
         'State': "QUEUED" }

msg.body = json.dumps(data)
print msg.body

# Insert the message to table first
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

# Submit the message to service bus queue
bus_service.send_queue_message(queue_name, msg)

# Receive a new message. Since peek_lock is False, the message will be read and 
# deleted from the queue in one atomic operation.
msgrec = bus_service.receive_queue_message(queue_name, False)
if not msgrec.body is None:
    print msgrec.body 
else:
    print "No message received within the timeout period"

# Receive a new message when peek_lock is True. We need to explicitly delete the
# message if we don't want it to re-appear on the queue.
msgrec = bus_service.receive_queue_message(queue_name, True)
if not msgrec.body is None:
    print msgrec.body 
    msgrec.delete() # in the lab, try commenting this line to see what happens
else:
    print "No message received within the timeout period"

