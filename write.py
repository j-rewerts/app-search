from swiftype_app_search import Client
import time

FILE = 'council_sample.csv'

print('Setting up connection')
client = Client(
    api_key='',
    base_endpoint='192.168.1.1:3002/api/as/v1',
    use_https=False,
)
print('connection established')

def main():
    with open(FILE, 'r') as report:
        for line in report:
            print('Indexing document')
            client.index_document('single-line-doc', {
                'contents': line
            })

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")