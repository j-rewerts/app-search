import json
from swiftype_app_search.exceptions import InvalidDocument

class AsyncClient:
    def __init__(self, client, api_key, base_endpoint='localhost:3002/api/as/v1', use_https=False):
        self.api_key = api_key

        uri_scheme = 'https' if use_https else 'http'
        self.base_url = "{}://{}".format(uri_scheme, base_endpoint)
        self.session = client
        self.headers = {
            'Authorization': "Bearer {}".format(api_key),
            'content-type': 'application/json; charset=utf8'
        }

    async def index_document(self, engine_name, document):
        """
        Create or update a document for an engine. Raises
        :class:`~swiftype_app_search.exceptions.InvalidDocument` when the document
        has processing errors
        :param engine_name: Name of engine to index documents into.
        :param document: Hash representing a single document.
        :return: dict processed document status
        """
        document_status = await self.index_documents(engine_name, [document])
        document_status = document_status[0]
        errors = document_status['errors']
        if errors:
            raise InvalidDocument('; '.join(errors), document)

        return {
            key: document_status[key]
            for key in document_status
            if key != 'errors'
        }

    async def index_documents(self, engine_name, documents):
        """
        Create or update documents for an engine.
        :param engine_name: Name of engine to index documents into.
        :param documents: Hashes representing documents.
        :return: Array of document status dictionaries. Errors will be present
        in a document status with a key of `errors`.
        """
        endpoint = "{}/engines/{}/documents".format(self.base_url, engine_name)
        data = json.dumps(documents)
        
        response = await self.session.post(endpoint, data=data, headers=self.headers)
        return await response.json()