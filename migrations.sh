#!/bin/bash

# Argument should be the description
flask db migrate -m "$1"

# Upgrades the database
flask db upgrade
