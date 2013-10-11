import getopt
import sys
import Constants
import random
import time
from DeviceMessenger import MsrPayload, MsrStorageQueueClient, MsrServiceBusQueueClient


def main(argv):
    iterations = 0
    try:
        opts, args = getopt.getopt(argv,"t:i",["type=","iterations="])
    except getopt.GetoptError:
        print 'usage: QueueClient.py --type Simple/Messaging --iterations 3'

    for opt, arg in opts:
        if opt in ('-i', '--iterations'):
            print arg + ' iterations has been selected'
            iterations = int(arg)
        if opt in ('-t','--type'):
            if arg.lower() == 'simple':
                # then do the simple queue
                print 'Storage queue has been selected'
                client = MsrStorageQueueClient.MsrStorageQueueClient()
            elif arg.lower() == 'messaging':
                # then do the messaging thing
                print 'Service bus queue has been selected'
                client = MsrServiceBusQueueClient.MsrServiceBusQueueClient()

    for i in range(0, iterations):
        # get the random lat and long
        # set the boundaries based on the picture of Europe
        # 49.88047802152056
        # 58.779591455820073
        # long
        # -12.656250499999942
        # 18.984374500000058
        lat = round(random.uniform(49.880478021520560, 58.779591455820073), 15)
        long = round(random.uniform(-12.656250499999942, 18.984374500000058), 15)
        # get the random temperature
        temp = random.randint(13, 30)
        # create the payload
        payload = MsrPayload.MsrPayload(long, lat, temp)
        # send the payload
        print(payload.GetJSONObject())
        client.SendQueueMessage(payload)
        # wait for a period of seconds before sending the next one
        time.sleep(5)

if __name__ == "__main__":
    main(sys.argv[1:])