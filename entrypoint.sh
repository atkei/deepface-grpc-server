#!/bin/bash

for i in {1..60}
do
  if piccolo migrations forwards face_service; then
    break
  fi

  if [[ $i -eq 60 ]]; then
    echo $(date -u +"%Y-%m-%d %H:%M:%S,%3N") Failed to complete db migrations. Exit
    exit 1
  fi

  echo $(date -u +"%Y-%m-%d %H:%M:%S,%3N") Failed to complete db migrations. Retry
  sleep 1s
done

exec python server.py
