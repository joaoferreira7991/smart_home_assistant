#!/bin/bash

# Note: migrations directory must be created, for that execute flask db init on the terminal.
#	If you want to reset the database models just remove the migrations directory and run this script.
# This script is used to migrate and update a new version of the model database, flask db.

# Check if directory migrations/ is created if not then create it.
if [ -d ./migrations ];then
	echo "migrations dir is present."
else
	echo "migrations dir not present."
	flask db init
fi

# Argument should be the description just like a commit in git
flask db migrate -m "$1"

# Upgrades the database
flask db upgrade
