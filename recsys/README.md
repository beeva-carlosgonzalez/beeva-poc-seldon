## Seldon benchmarks

*How to deploy [Seldon locally on Minikube (requires >8GB RAM)](../README_minikube.md)*

### Test Item Similarity for Movielens 100K

* Metric: MAP@10 (Mean Average Precision at 10)
* Algorithm: item similarity
* Dataset: Movielens 100K (subset u1)

#### Import dataset
```
kubectl create -f ~/seldon-server/kubernetes/conf/examples/ml100k/ml100k-import.json
```
*To import subset u1 you have to edit the file previously to launch seldon*

#### Train model
```
# Access to seldon-control shell
kubectl exec -it seldon-control /bin/bash

# Build model item-similarity
luigi --module seldon.luigi.spark SeldonItemSimilarity --local-schedule --client ml100k --startDay 1 --ItemSimilaritySparkJob-sample 1.0 --ItemSimilaritySparkJob-dimsumThreshold 0.0 --ItemSimilaritySparkJob-limit 100
```

#### Configure runtime
See [configure_runtime_scorer_isim](https://github.com/SeldonIO/seldon-server/blob/master/docker/examples/ml10m/create_ml10m_recommender.sh)


#### Generate keys
```
SELDONSERVERPOD=`kubectl get pods | grep seldon-server | cut -d' ' -f1`
sudo kubectl port-forward $SELDONSERVERPOD 8080
SELDONKEY=`seldon-cli keys --action list --client-name ml100k --scope all | cut -d' ' -f10 | tail -n1 | sed 's/[^A-Z0-9]//g'`
SELDONSECRET=`seldon-cli keys --action list --client-name ml100k --scope all | cut -d' ' -f4 | tail -n1 | sed 's/[^A-Z0-9]//g'`
# Open localhost:8080
curl http://localhost:8080/token?consumer_key=$SELDONKEY&consumer_secret=$SELDONSECRET
curl http://localhost:8080/users/625/recommendations?oauth_token=XXXX&algorithms=recommenders:MATRIX_FACTOR
```

#### Eval model
Use [RecommendationMetrics scripts](https://github.com/beeva-labs/beeva-poc-seldon/tree/master/recsys/RecommendationMetrics)
with [version](https://github.com/beeva-labs/beeva-poc-seldon/commit/dfe26aeae53c3e3ee7066a29b965e53bbf73bc09)
```
python SeldonTests.py --host=http://localhost:8080 --compareactionsfile=/home/enriqueotero/datasets/movielens/ml-100k/u1.test --consumerkey=$SELDONKEY --consumersecret=$SELDONSECRET --algorithm=itemsimilarity --insertactionsfile=/home/enriqueotero/datasets/movielens/ml-100k/u1.base
```

#### Results:
| Seldon version | Seldon Parameters | Test Parameters | MAP@10 | Missing results 
| --- | -----------| ---- | --- | ---
| 1.3.5 | diversityLevel=1, limit=100, threshold=0.5, sample=0.25, recent_actions=1 | dataset=ua, actions=100 | 0.01 | 11 empty users
| 1.3.5 | diversityLevel=1, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=ua, actions=100 | 0.05 | 89 empty users
| 1.3.5 | diversityLevel=1, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=100 | 0.054 | 0% missing users
| 1.3.5 | diversityLevel=1, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=100 (reverse) | 0.098 | 0% missing users
| 1.3.5 | diversityLevel=1, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=1000 (reverse) | 0.094 | 0% missing users
| 1.3.5 | diversityLevel=1, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=10 | 0.094 | 0% missing
| 1.3.5 | diversityLevel=1, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=1 | 0.083 | 0% missing,  406/4590=8.9% repeated
| 1.3.5 | diversityLevel=3, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=1, [commit](https://github.com/beeva-labs/beeva-poc-seldon/commit/4236661512a29f0ae719f9158014369cfdf7dd8c)| 0.083 | 0% missing, 391/4590=8.5% repeated
| 1.3.5 | diversityLevel=3, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=10, [commit](https://github.com/beeva-labs/beeva-poc-seldon/commit/c841c0edf4310c4b909fe8cebc2888d92d8f1a2b)| 0.099 | 0% missing, 324/4590=7.1% repeated
| 1.3.5 | diversityLevel=3, limit=100, threshold=0, sample=1, recent_actions=1 | dataset=u1, actions=100 | 0.059 | 0% missing, 244/4590=5.3% repeated

#### Conclusions: 
* (At the moment) we were not able to repeat our previous results with Seldon :( 
* MAP@10 we get for item-similarity and ml100k is low < 0.1 :(
* To be continued... :)
