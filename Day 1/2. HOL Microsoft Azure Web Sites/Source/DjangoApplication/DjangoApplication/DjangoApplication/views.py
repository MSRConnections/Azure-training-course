from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
from azure.storage import *
from DjangoApplication.settings import *
import base64
import urllib
import csv
import string
import json
from django.template.context import RequestContext


def earthquake(request):

    #load the earthquake data from internet
    csvgps = urllib.urlopen("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv")
    f = csvgps.read();
    with open('csvgps.csv','w') as temp:
        temp.write(f)

    length = 20

    data = [[0 for col in range(4)] for row in range(length)]
    reader = csv.reader(open("csvgps.csv"), delimiter=",")
    index = 0
    for line in reader:
        if index > 0 and index <= length:
            data[index - 1][0] = line[0]
            data[index - 1][1] = float(line[1])
            data[index - 1][2] = float(line[2])
            data[index - 1][3] = float(line[4])
        index = index + 1


    #load the template
    t = get_template('earthquake.html')
    d = RequestContext(request, {"location": {"latitude": '', "longitude": '', "data": data}})
   
    html = t.render(Context(d))

    return HttpResponse(html)

def home(request):
    return HttpResponse("Welcome to the Django Sample. Please add /earthquake to check all earthquakes in the last 30 days around the world.")


def webjob(request, latitude, longitude):

    #submit the location to queue for processing
    queue_service = QueueService(account_name=AZURE_ACCOUNT_NAME, account_key=AZURE_ACCOUNT_KEY)
    
    #create_queue to ensure the queue exists.
    queue_service.create_queue(AZURE_QUEUE_NAME)

    #create a base64 string to save the location data
    s = latitude +','+ longitude
    basecode = base64.b64encode(s)

    queue_service.put_message(AZURE_QUEUE_NAME, basecode)

    return  HttpResponse("OK")

def result(request, latitude, longitude):
    
    #check the existence of the data
    try:
        blob_service = BlobService(account_name=AZURE_ACCOUNT_NAME, account_key=AZURE_ACCOUNT_KEY)
        blob = blob_service.get_blob_to_path(AZURE_CONTAINER_NAME, AZURE_BLOB_NAME, AZURE_BLOB_NAME)    
        reader = csv.reader(open(AZURE_BLOB_NAME), delimiter=",")
    
        for line in reader:
            if line[1] != latitude or line[2] !=longitude:
                return HttpResponse('')
            else:
                break

        reader = csv.reader(open(AZURE_BLOB_NAME), delimiter=",")
        out = json.dumps( [ row for row in reader ] )
        return HttpResponse(out)
    
    except Exception:
        return HttpResponse('')
    
   
        

    