import argparse
from azure.storage import *

def main():
  parser = argparse.ArgumentParser(description='Split a data file and upload the pieces to blob storage')
  parser.add_argument('account', help='storage account name')
  parser.add_argument('key', help='storage account key')
  parser.add_argument('container', help='blob storage container')
  parser.add_argument('chunks', help='number of chunks to split to', type=int)
  parser.add_argument('csvfile', help='file to split and upload')

  args = parser.parse_args()

  blob_service = BlobService(account_name=args.account, account_key=args.key)
  blob_service.create_container(args.container)

  lines = 0
  for line in open(args.csvfile):
    lines += 1
  nRecords = lines - 1
  print '%s contains %d records' % (args.csvfile, nRecords)

  with open(args.csvfile) as csv:
    header = csv.readline()

    for i in xrange(args.chunks):
      chunkLen = nRecords / args.chunks
      if (i < nRecords % args.chunks):
          chunkLen += 1
      lines = [csv.next() for x in xrange(chunkLen)]
      blob = ''.join([header] + lines)
      blobname = 'chunk%d.csv' % (i+1)
      print 'Uploading %s/%s (%d records, %d bytes)' % (args.container, blobname, len(lines), len(blob))
      blob_service.put_blob(args.container, blobname, blob, x_ms_blob_type='BlockBlob')

if __name__ == '__main__':
  main()
