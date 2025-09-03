#!/bin/bash
#
# Basic bash script to save me some keystrokes when building and running docker containers

usage="Usage: $(basename "$0") [build|run|stop] \n 
build: Build the container \n
run: Run the container \n
stop: Stop and cleanup the container \n
Example to build the container: - ./$(basename "$0") -b"

if [[ -z $1 ]]; then
  echo -e $usage
  exit 1
else
  current_dir=$(pwd)
  case $1 in
    build) 
      sudo docker build -t jsnac .
      sudo docker image rm $(sudo docker image list -qf dangling=true)
      exit 0
      ;;
    run) 
      sudo docker run -it --name jsnac jsnac
      exit 0
      ;;
    stop)
      sudo docker stop $(sudo docker ps -qaf name=jsnac)
      sudo docker rm $(sudo docker ps -qaf name=jsnac)
      exit 0
      ;;
    *) error "Unexpected option ${flag}" ;;
  esac
fi