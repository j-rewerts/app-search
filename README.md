# App Search
Scripts related to Elasticsearch and AppSearch.

## Getting Started

1. Setup a virtual environment.
``` bash
python -m virtualenv venv
```

2. Source your environment.
``` bash
source ./venv/bin/activate
```

3. Install the requirements.
``` bash
pip install -r requirements.txt
```

4. View the help!
``` bash
python ./src/csv-to-elasticsearch.py -h
```

## Scripts

### CSV To Elasticsearch

This script lets you upload a large CSV to Elasticsearch. Every row represents a new document to be indexed. Currently, Elasticsearch's default tokenizer is used to prep the documents.

| Flag | Description | Required |
| ---- |:-----------:| --------:|
| -i | The index to write documents to | :heavy_check_mark: |
| -c | The Elasticsearch host string. Ex. '-c localhost:9200,localhost:9201,localhost:9202' | :heavy_check_mark: |
| -f | The CSV file. | :heavy_check_mark: |
| -h | Print the CLI help text. | :heavy_multiplication_x: |
| -u | The user to connect to Elasticsearch as. | :heavy_multiplication_x: |
| -p | The user's password. | :heavy_multiplication_x: |

#### Indexing Documents for Text Depot
``` bash
python src/csv-to-elasticsearch.py -i my_index -c https://textdepot.edmonton.ca/elasticsearch -f ~/Downloads/a_csv.csv -u es_user -p a_really_good_pw
```
