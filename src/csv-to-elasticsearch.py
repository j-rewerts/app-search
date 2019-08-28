from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import streaming_bulk
import time
from csv import reader


# Creating a tokenizer
# 'analysis': {
#     'analyzer': {
#         'my_ngram_analyzer': {
#             'tokenizer': 'my_ngram_tokenizer'
#         }
#     }
# },
# 'tokenizer': {
#     'my_ngram_tokenizer': {
#         'type': 'edgeNGram',
#         'min_gram': '2',
#         'max_gram': '10'
#     }
# }

def parse_reports(file):
    with open(file, 'r') as file_std:
        csv_reader = reader(file_std)

        for values in csv_reader:
            if csv_reader.line_num == 1:
                headers = values
            else:
                yield dict(zip(headers, values))


def create_index(client, index):
    try:
        client.indices.create(index=index)
    except TransportError as e:
        # ignore already existing index
        if e.error == 'resource_already_exists_exception':
            pass
        else:
            raise


def main():
    index = 'council_reports_3'
    es = Elasticsearch([
        {'host': '192.168.1.72', 'port': 9200},
        {'host': '192.168.1.72', 'port': 9201},
        {'host': '192.168.1.72', 'port': 9202}
    ])
    create_index(es, index)

    for ok, result in streaming_bulk(es, parse_reports('council_meta.txt'), index=index):
        action, result = result.popitem()
        doc_id = '/%s/doc/%s' % (index, result['_id'])

        if not ok:
            print("Failed to %s document %s: %r" % (action, doc_id, result))
        else:
            print(doc_id)


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start
    print(f'Program completed in {elapsed:0.5f} seconds.')
