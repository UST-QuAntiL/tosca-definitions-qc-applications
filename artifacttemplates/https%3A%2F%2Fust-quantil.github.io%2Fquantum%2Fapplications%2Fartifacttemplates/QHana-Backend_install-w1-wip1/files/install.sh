#!/bin/bash

IFS=';' read -ra NAMES <<< "$DAs";
for i in "${NAMES[@]}"; do
  echo "KeyValue-Pair: "
  echo $i
  IFS=',' read -ra entry <<< "$i";
    echo "Key: "
    echo ${entry[0]}
    echo "Value: "
    echo ${entry[1]}

  # find the executable jar file
  if [[ "${entry[1]}" == *.jar ]];
  then
    # copy the executable to /qhana_backend
    mkdir /qhana_backend
    cp $CSAR${entry[1]} /qhana_backend/qhana_backend.jar
  fi
done