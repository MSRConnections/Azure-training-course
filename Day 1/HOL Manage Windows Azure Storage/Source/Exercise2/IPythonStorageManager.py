#this sample illustrates fundamentals of how to use Azure to create, read and delete files within Blob Storage and Table Storage

#first we import modules we require
from azure.storage import *
import os
import csv
import numpy
from collections import defaultdict
import time

#put your account name and key here
account = 'trainingdemostorage'
key = 'mdJnNXPYS1cC5T4pf+9yva/UJ64sU1giJQ0clXoWHszU6i3sS3CZVmQaHctL1VbE9I7HeOODPv5HXTqVYY52nQ=='
containername = 'samplecontainer'

#get a handle to your account
blob_service = BlobService(account_name=account, account_key=key)

#list all blobs of the container
blobs = blob_service.list_blobs(containername)
for blob in blobs:
    print(blob.name)
    print(blob.url)
   
#create a new file a blob into a container
open(r'sample2.txt', 'w').write("This is another sample")

#upload the blob into the container
sampleblob2 = open(r'sample2.txt', 'r').read()
blob_service.put_blob(containername, 'sample2.txt', sampleblob2, x_ms_blob_type='BlockBlob')
#you can check the azure explorer to find the sample2.txt file

#then we can remove sample2.txt
os.remove(r'sample2.txt')
#delete the blob remotely
blob_service.delete_blob(containername, 'sample2.txt')
#check the azure storage explorer again, the file is removed.

#we can also download a csv file to local
csv_file = 'cut_diamonds.csv'
csvblob = blob_service.get_blob(containername, csv_file)
with open(csv_file, 'w') as f:
    f.write(csvblob)


#then we draw a scatter from the csvfile
columns = defaultdict(list) #we want a list to append each value in each column to

with open(csv_file) as f:
    reader = csv.DictReader(f) #create a reader which represents rows in a dictionary form
    for row in reader: #this will read a row as {column1: value1, column2: value2,...}        
        for (k,v) in row.items(): #go over each column name and value 
            columns[k].append(v) #append the value into the appropriate list based on column name k

carat = np.array(columns['Carat'])
price = np.array(columns['Price'])
scatter(carat,price,marker ='o',color='#ff0000')

#Next we are going to demostrate the table storage management in Windows Azure
#we can add top 100 rows of the cut_diamond csv to a table storage

#get a handle to your account
table_service = TableService(account_name=account, account_key=key)
table_name = 'diamondtable';

#delete the table for temporary data
result = table_service.delete_table(table_name)

# create a new table to save all entities.
result = table_service.create_table(table_name)


#attention: more code need to write if you want to execute all the time at the same time.
#when you call delete_table or create_table, it takes some time for Windows Azure to finish the opration
#you must check the operation status before you can execute the following code!    

#then we insert the top 100 diamond into the table, we set PartitionKey to be each diamonds' color and RowKey to be the index
index = 0
with open(csv_file) as f:
    reader = csv.DictReader(f) #create a reader which represents rows in a dictionary form
    for row in reader: #this will read a row as {column1: value1, column2: value2,...}        
        entity = Entity()
        entity.PartitionKey = row['Color']
        entity.RowKey= str(index)
        entity.Clarity = row['Clarity']
        entity.Cut = row['Cut']
        entity.Carat = row['Carat']
        entity.Price = row['Price']
        table_service.insert_entity(table_name, entity)
        print row
        index=index+1
        if index >= 100:
            break
#we can check the azure storage explore to query all entities that we inserted.

#we can also query all table entities with diamonds' color = 'D'
diamonds = table_service.query_entities(table_name, "PartitionKey eq 'D'")
for d in diamonds:
    print(str(d.Cut),str(d.PartitionKey),str(d.Clarity),str(d.Carat),'$'+ str(d.Price))

