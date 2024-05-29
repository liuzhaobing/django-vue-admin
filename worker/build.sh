#!/bin/bash
name="myroki-test-worker-nlp"
project="$name"
tag=`date +%Y%m%d_%H%M%S`
docker build -f Dockerfile -t $project:$tag .
