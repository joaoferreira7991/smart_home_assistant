web: flask db init; flask db migrate -m "sample"; flask db upgrade; gunicorn --worker-class eventlet -w 1 smart-home-assistant:app
