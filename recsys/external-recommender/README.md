## Deploy external recommender


### Launch Seldon
`./seldon-up.sh`

### Create client
`kubectl create -f ../conf/examples/ml100k/ml100k-import.json`

### Build model

* Our example is a [python recommendation microservice](http://docs.seldon.io/api-microservices.html#content-recommendation#recommender-python).

### Build docker image
`sudo make build_image`

* Last Dockerfile command calls [start_recommendation_microservice](https://github.com/SeldonIO/seldon-server/blob/master/docker/pyseldon/scripts/start_recommendation_microservice.py) with default port 

### Push docker image
`sudo make push_to_dockerhub`

### Generate the deployment descriptor
`./run_recommendation_microservice.sh dsstne-example beevaenriqueotero/seldon-dsstne 0.2 ml100k`
