#!/bin/bash
#
# Basic bash script to save me some keystrokes when building and running docker containers

usage="Usage: $(basename "$0") -bcr \n 
-b: Build and run the container \n
-c: Stop and cleanup the container \n
-r: Stop, Rebuild and re-run the container \n
Example to build the container: - ./$(basename "$0") -b"

if [[ -z $1 ]]; then
  echo -e $usage
  exit 1
fi

while getopts 'bcr' flag; do
  case "${flag}" in
    b) 
      sudo docker build -t jsnac .
      sudo docker image rm $(sudo docker image list -qf dangling=true)
      sudo docker run -it --name jsnac jsnac
      exit 0
      ;;
    c) 
      sudo docker stop $(sudo docker ps -qaf name=jsnac)
      sudo docker rm $(sudo docker ps -qaf name=jsnac)
      exit 0
      ;;
    r)
      sudo docker stop $(sudo docker ps -qaf name=jsnac)
      sudo docker rm $(sudo docker ps -qaf name=jsnac)
      sudo docker build -t jsnac .
      sudo docker image rm $(sudo docker image list -qf dangling=true)
      sudo docker run -it --name jsnac jsnac
      exit 0
      ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done