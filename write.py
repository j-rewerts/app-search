from swiftype_app_search import Client

print('Setting up connection')
client = Client(
    api_key='',
    base_endpoint='162.106.81.175:3002/api/as/v1',
    use_https=False,
)
print('connection established')

with open('council_reports.csv', 'r') as report:
    for line in report:
        print('Indexing document')
        client.index_document('single-line-doc', {
            'contents': line
        })