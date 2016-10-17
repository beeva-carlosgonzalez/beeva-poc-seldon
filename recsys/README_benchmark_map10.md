### Seldon benchmarks

* Metric: MAP@10 (Mean Average Precision at 10)
* Algorithm: item similarity
* Dataset: Movielens 100K (subset u1)

*How to deploy [Seldon locally on Minikube (requires >8GB RAM)](../README_minikube.md)*


#### Train model
```
# Access to seldon-control shell
kubectl exec -it seldon-control /bin/bash

# Build model item-similarity
luigi --module seldon.luigi.spark SeldonItemSimilarity --local-schedule --client ml100k --startDay 1 --ItemSimilaritySparkJob-sample 1.0 --ItemSimilaritySparkJob-dimsumThreshold 0.0 --ItemSimilaritySparkJob-limit 100
```

#### Configure runtime
See [configure_runtime_scorer_isim](https://github.com/SeldonIO/seldon-server/blob/master/docker/examples/ml10m/create_ml10m_recommender.sh)


#### Eval model
Use [RecommendationMetrics scripts](https://github.com/beeva-labs/beeva-poc-seldon/tree/master/recsys/RecommendationMetrics)
with [version](https://github.com/beeva-labs/beeva-poc-seldon/commit/dfe26aeae53c3e3ee7066a29b965e53bbf73bc09)
```
python SeldonTests.py --host=http://localhost:8080 --compareactionsfile=/home/enriqueotero/datasets/movielens/ml-100k/u1.test --consumerkey=$SELDONKEY --consumersecret=$SELDONSECRET --algorithm=itemsimilarity --insertactionsfile=/home/enriqueotero/datasets/movielens/ml-100k/u1.base
```

#### Results:
| Seldon version | Parameters | MAP@10 
| --- | -----------| ---- 
| 1.3.5 | dataset=ua, diversityLevel=1, limit=100, threshold=0.5, sample=0.25, actions=100, recent_actions=1 | 0.01 (11 empty users)
| 1.3.5 | dataset=ua, diversityLevel=1, limit=100, threshold=0, sample=1, actions=100, recent_actions=1 | 0.05 (89 empty users)
| 1.3.5 | dataset=u1, diversityLevel=1, limit=100, threshold=0, sample=1, actions=100, recent_actions=1 | 0.054 (0 empty users)
| 1.3.5 | dataset=u1, diversityLevel=1, limit=100, threshold=0, sample=1, actions=100 (reverse), recent_actions=1 | 0.098 (0 empty users)
| 1.3.5 | dataset=u1, diversityLevel=1, limit=100, threshold=0, sample=1, actions=1000 (reverse), recent_actions=1 | x (0 empty users)
| 1.3.5 | dataset=u1, diversityLevel=1, limit=100, threshold=0, sample=1, actions=5 (reverse), recent_actions=1 | x (0 empty users)

#### Conclusions: 
* (At the moment) we were not able to repeat our previous results with Seldon :( 
* MAP@10 we get for item-similarity and ml100k is very low < 0.01 :(
* To be continued... :)