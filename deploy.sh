#!/bin/bash

# First argument is the message to be commited
# Example usage: deploy.sh "First Commit" 
if [ ! $1 ];then
    echo "Missing first argument!"
else
    git add .
    git commit -m $1
    git push heroku master
    heroku logs --tail
fi