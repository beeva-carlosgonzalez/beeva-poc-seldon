## Deploy external recommender

### Build docker image
`sudo make build_image`

* Our example is a [python recommendation microservice](http://docs.seldon.io/api-microservices.html#content-recommendation#recommender-python).
* Last Dockerfile command calls [start_recommendation_microservice](https://github.com/SeldonIO/seldon-server/blob/master/docker/pyseldon/scripts/start_recommendation_microservice.py) with default port 

### Push docker image
`sudo make push_to_dockerhub`

### Generate the deployment descriptor
`./run_recommendation_microservice.sh dsstne-example seldon-dsstne 0.1 ml100k`

### Launch Seldon
`./seldon-up.sh`
