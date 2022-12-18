#!/bin/sh
curl -vX POST -d @cdc_config.json --header "Content-Type: application/json" http://localhost:8080/v3/sources/public/default/transactions-cdc 
