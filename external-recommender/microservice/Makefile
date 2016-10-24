SELDON_PYTHON_PACKAGE_VERSION=latest
SELDON_DSSTNE_EXAMPLE_IMAGE_VERSION=0.1
IMAGE_NAME=	beevaenriqueotero/seldon-dsstne
IMAGE_FOLDER=.

Dockerfile: Dockerfile.in
	@cat Dockerfile.in | \
		sed 's/%SELDON_PYTHON_PACKAGE_VERSION%/$(SELDON_PYTHON_PACKAGE_VERSION)/' > Dockerfile

build_image: Dockerfile
	docker build --force-rm=true -t $(IMAGE_NAME):$(SELDON_DSSTNE_EXAMPLE_IMAGE_VERSION) .

push_to_dockerhub:
	cd ${IMAGE_FOLDER} ; docker login -u beevaenriqueotero && \
		docker push $(IMAGE_NAME):$(SELDON_DSSTNE_EXAMPLE_IMAGE_VERSION)

clean:
	@rm -fv Dockerfile
