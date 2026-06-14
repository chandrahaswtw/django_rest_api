#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

# Option	            Meaning
# uwsgi	                Start the uWSGI server
# --socket :9000	    Listen on TCP port 9000 for incoming requests
# --workers 4	        Create 4 worker processes to handle requests concurrently
# --master	            Run a master process that manages worker processes
# --enable-threads	    Allow Python threads inside worker processes
# --module app.wsgi	    Load the WSGI application from app/wsgi.py

# --workers 4 This spins up 4 workers, all share the same port. 
# Basically all these workers present in the same container.
# uWSGI acts as a load balancer for these workers.

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi