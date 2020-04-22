#!/bin/bash

# First argument should be the name of the project to be uploaded
# Second argument should be the string to add to Commit
# Example usage: deploy.sh flask-tutorial "First Commit"


virtual/bin/pip freeze > requirements.txt
flask db init
git init
git add .
git commit -m $2
heroku create $1
git push heroku master
heroku ps:scale web=1
