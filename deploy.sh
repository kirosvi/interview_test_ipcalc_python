#!/bin/bash
NAME=ipcalc-app

helm upgrade ${NAME} \
  ./helm \
  --install \
  --create-namespace \
  --namespace=${NAME} \
  --set global.tier=prod
