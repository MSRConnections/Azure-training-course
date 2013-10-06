#this sample illustrates fundamentals of how to use Azure to create, read and delete files within Blob Storage

#first we import Azure.Storage modules (and the OS module for IO)
from azure.storage import *
import credentials
import StorageManager


class Tables:

    # create class and pass in a default table name if none specified
    def __init__(self, account_name, table_name = "auditrecord"):
        self.table_name = table_name
        serviceManager = StorageManager.StorageManager(account_name)
        self.table_service = TableService(account_name, serviceManager.GetAccountCredentials())

    # create the table not checking here to see whether the table exists already
    def CreateTable(self):
        # create an audit record entity based on collecting information on applications
        # use the PartitionKey as the data centre name and RowKey as a simple index
        self.table_service.create_table(self.table_name)
        print 'creating table ' + self.table_name

    # deletes the table if it exists
    def DeleteTable(self):
        # this won't report if it fails so it's safe to execute
        self.table_service.delete_table(self.table_name)
        print 'deleting table ' + self.table_name

    # adds the first test entity with a unique table partition key
    def AddTestEntity1(self):
        # first entity is an error entity
        entity1 = Entity()
        entity1.PartitionKey = 'North Europe'
        entity1.RowKey = '1'
        entity1.description = 'Application failed to connect to server'
        entity1.type = 'error'
        # add the entities to the table service
        self.table_service.insert_entity(self.table_name, entity1)
        print 'adding test entity 1'

    # adds the second test entity with a unique partition key
    def AddTestEntity2(self):
        # second entity is an info entity
        entity2 = Entity()
        entity2.PartitionKey = 'East US'
        entity2.RowKey = '2'
        entity2.description = 'Successful user authentication'
        entity2.type = 'information'
        # add in additional column to show schemaless dynamic nature
        entity2.attempts = '1'
        # show this in a REPL or debug to show the schema changes and the null value being passed to the previous entity
        self.table_service.insert_entity(self.table_name, entity2)
        print 'adding test entity 2'

    # update the second entity
    def UpdateEntity2(self):
        records = self.table_service.query_entities(self.table_name, "PartitionKey eq 'East US'", 'PartitionKey,RowKey,description')
        # show an update of an entity
        records[0].attempts = '2'
        self.table_service.update_entity(self.table_name, records[0].PartitionKey, records[0].RowKey, records[0])
        print 'updating test entity 2'

    # display all of the entities
    def DisplayEntities(self):
        records = self.table_service.query_entities(self.table_name, "PartitionKey eq 'North Europe' or PartitionKey eq 'East US'", 'description')
        print 'the table descriptions are: '
        for record in records:
            print('\t' + record.description)

