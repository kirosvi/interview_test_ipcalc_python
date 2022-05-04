I decide to not spending a lot of time for creating prototype and used existing library for working with networks in python and existing HTTP server. (the only limitation is about _ipaddress_ library. it need some test on larger instance because there are some problems when it trying to calculate large networks /8 and larger)
For deploy I used Helm with my own chart for basic applications.
Images already builded and pushed in _docker.io_ registry.

### Possible improvements
- create a nice frontend for users who not like cli and love GUI
- rewrite code without using python library for working with subnetworks
- add json logs for app

## How to run

### K8s with cert

requirements:
- needs installed ingress with class "nginx" by default (could be changed via values.yaml)
    ```
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm install ingress-nginx ingress-nginx/ingress-nginx
    ```

- needs installed cert-manager
    ```
    $ kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.0/cert-manager.crds.yaml
    $ helm repo add jetstack https://charts.jetstack.io
    $ helm install my-release --namespace cert-manager --version v1.8.0 jetstack/cert-manager
    ```

Installation in k8s:
```
./deploy.sh
```

- If you want deploy with valid certificate, then you should before deploy:
    - delete __issuer.yaml__ in template directory
    - remove annotation for custom issuer and set option _acme.prod: true_ for ingress in __values.yaml__
    - change hostname for ingress in __values.yaml__

## Q&A

- _Imagine this server being deployed in an infrastructure. What would be the security concerns you would raise?_
    * if we get a plenty of request from greedy users that whant to get info about their subnetwork:
        - we could set rate limits for requests by ip
        - we need to check if we have enough resources to scale our cluster
        - set more replicas in deployment
        - get more resources for each instance
        - optimize python code with C/C++ implementations
        - or, finaly, rewrite all applications on another more suitable language
    * if we got some DDOS attack on our service from not well-minded users:
        - we should set rate limit for requests by ip
        - implement caching feature for similar requests
        - optimize code or rewrite it on more suitable laguage for HL
        - we should check if we running container under root user and fix it (this is really bad idea)
    * beccause of using third-party librarys in python we have probability of ending of support for this parts:
        - we could rewrite their logic in our way
        - we could just freeze versions of our requirements (it wouldn't be the best descision but working in some cases) and save artifacts in some storage for later uses
- _How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?_
    Actually I didn't saw requirement to write some kind of monolith in one container. so it already written and packaged in separate containers and you could scale it or add another separate services for new feature needs.


