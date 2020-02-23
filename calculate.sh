#!/bin/bash

UUID=$(curl http://localhost:5000/calculations -H "Content-Type: application/json" -d @calculation.json -s \
      | sed -nE 's/.*"uuid": "(.*)"}/\1/p')
echo $UUID
curl http://localhost:5000/calculations/$UUID
