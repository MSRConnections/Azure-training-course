import argparse
from azure.storage import *

def main():
  parser = argparse.ArgumentParser(description='Split a data file and upload the pieces to blob storage')
  parser.add_argument('account', help='storage account name')
  parser.add_argument('key', help='storage account key')
  parser.add_argument('container', help='blob storage container')
  parser.add_argument('chunk', help='number of chunk to upload to', type=int)

  args = parser.parse_args()
  blobname = 'chunk%d.csv' % args.chunk

  blob_service = BlobService(account_name=args.account, account_key=args.key)
  blob_service.create_container(args.container)

  lines = 0
  for line in open(blobname):
    lines += 1
  nRecords = lines - 1
  print '%s contains %d records' % (blobname, nRecords)

  
  blob = open(blobname).read()
  print 'Uploading %s/%s (%d bytes)' % (args.container, blobname, len(blob))
  blob_service.put_blob(args.container, blobname, blob, x_ms_blob_type='BlockBlob')

if __name__ == '__main__':
  main()
