from swiftype_app_search import Client
import time
import csv

FILE = 'council_reports.csv'
NUM_DOCS = 10
SEARCH_ENGINE = 'temp-council-6'

def main():
    print('Setting up connection')
    client = Client(
        api_key='',
        base_endpoint='192.168.1.1:3002/api/as/v1',
        use_https=False,
    )
    print('connection established')

    docs = []
    with open(FILE, 'r', encoding='utf-8-sig') as file_std:
        csv_reader = csv.reader(file_std, delimiter=',')
        row_num = 0

        # Read every line, sending NUM_DOCS documents at once.
        for line in csv_reader:
            if row_num == 0:
                columns = line
                print(f'Column names are {", ".join(line)}')
            elif row_num % NUM_DOCS == 0:
                print('Indexing documents {} through {}'.format(row_num-NUM_DOCS, row_num))
                docs.append(dict(zip(columns, line)))
                responses = client.index_documents(SEARCH_ENGINE, docs)
                for response in responses:
                    if 'errors' in response and len(response.get('errors')) > 0:
                        print(response.get('errors'))
                        return
                docs = []
            else:
                docs.append(dict(zip(columns, line)))
            row_num += 1


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")