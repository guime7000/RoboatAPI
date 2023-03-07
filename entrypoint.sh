#!/bin/bash
set -e

case $1 in
  setup)
    echo "Setup archives"
    python Tools/archiveFiles_initial_creator.py
    echo "Setup positions"
    python Tools/positionFiles_initial_creator.py
    ;;
  server)
    echo "Running API"
    exec uvicorn Src.roboatAPI:app --host "0.0.0.0"
    ;;
  *)
    echo "Running server command: $*"
    exec "$@"
    ;;
esac
