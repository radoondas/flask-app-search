from json import loads
from itertools import zip_longest
from elastic_app_search import Client


def batching_function(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


# Configuration
MAX_BATCH_SIZE = 100
host_identifier = 'localhost:3002/api/as/v1'
api_key = 'private-key'
engine_name = 'flask-app-search'
file_name='movies.json'

client = Client(
    api_key=api_key,
    base_endpoint=host_identifier,
    use_https=False
)

f = open(file_name, "r")
document=f.read()
records=loads(document)
batched_records=list(batching_function(records,MAX_BATCH_SIZE))
number_of_batches=len(batched_records)
print("Indexing "+str(len(records))+" records using "+str(number_of_batches)+" batches, each carrying up to "+str(MAX_BATCH_SIZE)+" documents")
for i in range(number_of_batches):
    indexing_response=client.index_documents(engine_name, batched_records[i])
    print("...batch "+str(i+1)+" with "+str(len(list(filter(None, batched_records[i])) ))+" documents completed"),
    number_of_responses=len(indexing_response)
    errors_encountered=0
    for j in range(number_of_responses):
        if len(indexing_response[j].get("errors")) != 0:
            errors_encountered+=1
    if errors_encountered == 0:
        print("with no errors")
    else:
        print("with "+str(errors_encountered)+" errors")
