from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import streaming_bulk
import time
import getopt
import sys
import csv
csv.field_size_limit(sys.maxsize)


help = """
This python utility helps with uploading CSV files of any size to Elasticsearch. This has been tested up to ~2GB. Currently, all fields in the document are indexed and treated as text. In the future, controlling how the fields are indexed from the command line would be a handy feature.

Example on localhost
python csv-to-elasticsearch.py -i my-index -c localhost:9200,localhost:9201 -f my.csv

Example over https
python csv-to-elasticsearch.py -i my-index -c https://sub.domain.ca/es -f my.csv

Required fields
-i (--index) The index to write documents to.
-c (--connect) The Elasticsearch host string.
  Ex. '-c localhost:9200,localhost:9201,localhost:9202'
-f (--file) The CSV file. 

Optional fields
-h (--help) Print this helpful text field.
-u (--user) The user to connect to Elasticsearch as.
-p (--password) The user's password.
"""


def parse_reports(file):
    with open(file, 'r') as file_std:
        csv_reader = csv.reader(file_std)

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


def parse_hosts(hosts):
    """
    Parses a comma delimited string of hosts.
    Ex. localhost:9200,localhost:9201,localhost:9202

    :param str hosts The hosts string.
    :return List An Elasticsearch list of hosts.
    """
    return hosts.split(',')


def parse_args(args):
    """
    Parses the command line arguments. See 'help' for details.
    """
    short_opts = 'hi:c:f:u:p:'
    long_opts = [
        'help',
        'index=',
        'connect=',
        'file=',
        'user=',
        'password='
    ]
    index, hosts, csv_file, user, password = None, None, None, None, None
    try:
        opts, args = getopt.getopt(args, short_opts, long_opts)
    except getopt.GetoptError:
        print(help)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ('-i', '--index'):
            index = arg
        elif opt in ('-c', '--connect'):
            hosts = arg
        elif opt in ('-f', '--file'):
            csv_file = arg
        elif opt in ('-u', '--user'):
            user = arg
        elif opt in ('-p', '--password'):
            password = arg
        else:
            print('Unknown flag: {}'.format(opt))
            sys.exit(2)

    if not index:
        print('-i is required')
        print(help)
        sys.exit(2)
    if not hosts:
        print('-c is required')
        print(help)
        sys.exit(2)
    if not csv_file:
        print('-f is required')
        print(help)
        sys.exit(2)
    return index, hosts, csv_file, user, password


def main(index, hosts, csv_file, user, password):
    hosts = parse_hosts(hosts)
    es = None
    if user and password:
        es = Elasticsearch(hosts, http_auth=(user, password))
    else:
        es = Elasticsearch(hosts)
    create_index(es, index)

    for ok, result in streaming_bulk(es, parse_reports(csv_file), index=index, max_retries=5):
        action, result = result.popitem()
        doc_id = '/%s/doc/%s' % (index, result['_id'])

        if not ok:
            print('Failed to %s document %s: %r' % (action, doc_id, result))
        else:
            print(doc_id)


if __name__ == '__main__':
    start = time.perf_counter()
    index, hosts, csv_file, user, password = parse_args(sys.argv[1:])
    main(index, hosts, csv_file, user, password)
    elapsed = time.perf_counter() - start
    print(f'Program completed in {elapsed:0.5f} seconds.')
