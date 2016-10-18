## Deploy and Test Seldon locally on Minikube

### Deploy Seldon on localhost

Successfully tested on Ubuntu 16.04 with >8GB RAM

#### Prerequisite 1: Install Minikube:
*Requires Virtualbox or KVM*
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.10.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
# Test minikube start --memory=6000
```

#### Prerequisite 2: Download kubectl (kubernetes):
Recommended version: v1.3.8
```
curl -O https://storage.googleapis.com/kubernetes-release/release/v1.3.8/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl
```

#### Prerequisite 3: Download Seldon:
Recommended version: v1.3.5

```
wget https://github.com/SeldonIO/seldon-server/archive/v1.3.5.zip
sudo apt-get install unzip
unzip v1.3.5.zip
mv seldon-server-1.3.5/ ~/seldon-server
```

#### Prerequisite 4: Configure Python libraries
Recommended: virtualenv

#### Launch Minikube
```
minikube start --memory=8000
```

#### Launch Seldon:
```
# Add Seldon to path
cd ~/seldon-server/kubernetes/bin/; export PATH=$PATH:`pwd`

# Configure config files
cd ../conf
make clean conf

# Launch Seldon
seldon-up.sh
```
![seldon_up.sh output](static/seldon_up.png "seldon-up.sh output")

Check that Seldon is OK. And [test it!](https://github.com/beeva-labs/research-lab-private/tree/master/recsys/seldon-kubernetes#import-new-dataset)



#### End:
Close Seldon
```
seldon-down.sh
```
Delete Minikube
```
minikube delete
```

#### Troubleshooting
* Seldon Server (or any other pod) hangs at pending. `kubectl describe pod seldon-server-...` says: *"failed to fit in any node fit failure on node (minikube): Insufficient Memory"*
  * Increase minikube RAM allocation to 8G: `minikube start --memory=8000`
  * https://github.com/SeldonIO/seldon-server/issues/23
