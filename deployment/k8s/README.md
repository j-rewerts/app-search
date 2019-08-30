

## Installation

The bulk of this guide was pulled from Elastic's official [documentation](https://www.elastic.co/elasticsearch-kubernetes).

1. Ensure your user has the Cluster Admin role. In GKE, run 
``` bash
kubectl create clusterrolebinding \
  cluster-admin-binding \
  --clusterrole=cluster-admin \
  --user=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
```

2. Install the Elastic Cloud on Kubernetes Operator:
``` bash
kubectl apply -f https://download.elastic.co/downloads/eck/0.9.0/all-in-one.yaml
```

3. From the same directory this `README.md` file is in, run:
``` bash
kubectl apply -f yaml/ --namespace=textsearch
```

This creates the Elasticsearch cluster, as well as deploying Kibana. 

4. Get the default Elasticsearch user's credentials:
``` bash
PASSWORD=$(kubectl get secret textsearch-es-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)
```

5. To access the service, forward the containers port to your local machine **using in a new terminal**:
``` bash
kubectl port-forward service/textsearch-es-es-http 9200
```

6. Send the following cUrl request **in the same terminal you've stored your Elastic user's password in**:
``` bash
curl -u "elastic:$PASSWORD" -k "https://localhost:9200"
```

You should see a JSON document with some information, including the tagline `You Know, for Search`.

7. Now check out Kibana. First, forward the port for the Kibana service:
``` bash
kubectl port-forward service/textsearch-kibana-kb-http 5601
```

8. Visit https://localhost:5601. Notice these are HTTPS Urls. You will likely have to click through a warning screen, as the certificates this is using are self-signed. Enter username `elastic` and use the password you retrieved before (`echo $PASSWORD`).
