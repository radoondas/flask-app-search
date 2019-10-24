import json


with open('movies.json') as infile:
  o = json.load(infile)
  chunkSize = 100
  for i in xrange(0, len(o), chunkSize):
    with open('file_' + str(i//chunkSize) + '.json', 'w') as outfile:
      json.dump(o[i:i+chunkSize], outfile)
