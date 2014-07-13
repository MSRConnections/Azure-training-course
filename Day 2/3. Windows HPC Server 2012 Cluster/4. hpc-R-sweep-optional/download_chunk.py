import argparse
from azure.storage import *

def main():
  parser = argparse.ArgumentParser(description='Split a data file and upload the pieces to blob storage')
  parser.add_argument('account', help='storage account name')
  parser.add_argument('key', help='storage account key')
  parser.add_argument('container', help='blob storage container')
  parser.add_argument('chunk', help='chunk number to download', type=int)

  args = parser.parse_args()
  blobname = 'chunk%d.csv' % args.chunk

  blob_service = BlobService(account_name=args.account, account_key=args.key)
  blob = blob_service.get_blob(args.container, blobname)

  with open(blobname, 'w') as csv:
    csv.write(blob)

if __name__ == '__main__':
  main()
