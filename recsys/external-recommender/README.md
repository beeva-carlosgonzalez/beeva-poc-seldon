## Deploy external recommender

### Build docker image
`sudo make build_image`

### Push docker image
`sudo make push_to_dockerhub`

### Generate the deployment descriptor
`./run_recommendation_microservice.sh dsstne-example seldon-dsstne 0.1 ml100k`

### Launch Seldon
`./seldon-up.sh`
