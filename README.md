I decided to not spend a lot of time creating prototypes and used the existing library for working with networks in python and Flask. (the only limitation is about the _ipaddress_ library. it need some test on larger instance and maybe paly with some parameters, because there are some problems when it trying to calculate networks larger than /8)

For deployment I used Helm with my own basic chart for applications (it included some necessary k8s features to be sure to use by default).

Images already builded and pushed in _docker.io_ registry, so basically you could just deploy it in you cluster or you could build them and push in your registry (don't forget to update __values.yaml__ for right path to images)




### Possible improvements
- create a nice frontend for users who not like cli and love GUI
- rewrite code without using python library for working with subnetworks
- add json logs for app

## How to run

### K8s with cert

requirements:
- installed [ingress](https://artifacthub.io/packages/helm/ingress-nginx/ingress-nginx) with class "nginx" by default (could be changed via __values.yaml__)
- installed [cert-manager](https://artifacthub.io/packages/helm/cert-manager/cert-manager)
- for acme with dns01 needed [external-dns](https://artifacthub.io/packages/helm/bitnami/external-dns)

> if you want use your own dns name, change it in __values.yaml__ and then use it in instructions below instead of "test.k8s.local.dev"

Installation in k8s:

```
./deploy.sh
```

- If you want deploy with valid certificate, then you should before deploy:
    - change hostname for ingress in __values.yaml__
    - remove annotation for custom issuer __cert-manager.io/issuer: *issuerName__ for ingress in __values.yaml__
    - for acme with dns01:
        disable "issuer.selfsigned.enabled=false"
    - for acme through http01 additionally (unfortunately I don't have available domain or external host for testing exactly for this task right now, but something like this I've done before in project with our customer):
        disable "issuer.selfsigned.enabled=false" and enable "issuer.acmeHttp.enabled=true" in __values.yaml__

## Usage
- in cli with curl:

```
curl -k 'https://test.k8s.local.dev/calc?net=192.168.1.19/30'
```

- in browser:
    - add "${YOUR_INGRESS_IP} test.k8s.local.dev" to hosts file
    - open  [test.k8s.local.dev](https://test.k8s.local.dev) and approve certificate to trust on your machine (just in browser or download and add to host CA, instructions could be found [here](https://www.google.com/search?q=add+self+signed+certificate+to+trusted&oq=add+self+signed+certificate+to+trusted&aqs=chrome..69i57j0i512j69i59j0i512l7.7201j0j7&sourceid=chrome&ie=UTF-8))
    - and now you could open [https://test.k8s.local.dev/calc?net=192.168.1.19/30](https://test.k8s.local.dev/calc?net=192.168.1.19/30)

## Q&A

- _Imagine this server being deployed in an infrastructure. What would be the security concerns you would raise?_
    * first of, all get rid of _ipaddress_ library for using this project in production.
    * if we get a plenty of request from greedy users that want to get info about their subnetwork:
        - we could set rate limits for requests by ip
        - we need to check if we have enough resources to scale our cluster
        - set more replicas in deployment
        - get more resources for each instance
        - optimise python code with C/C++ implementations
        - or, finally, rewrite all applications on another more suitable language
    * if we got some DDOS attack on our service from not well-minded users:
        - we should set rate limit for requests by ip
        - implement caching feature for similar requests
        - optimise code or rewrite it on more suitable language for HL
        - we should check if we running container under root user and fix it (this is really bad idea)
    * because of using third-party libraries in python we have probability of ending of support for this parts:
        - we could rewrite their logic in our way
        - we could just freeze versions of our requirements (it wouldn't be the best decision but working in some cases) and save artefacts in some storage for later uses
- _How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?_
    Actually I didn't see a requirement to write some kind of monolith in one container. so it is already written and packaged in separate containers and you could scale it or add another separate service for new feature needs. Also it works in specific location and has args for request, so if needed it's possible to expand for new args or add different locations with another logic.
