# docker-celery-api

THis code is on Fast api with celery for background tasks using redis as broker.

To execute the code use following command

# docker-compose up -d --f

it will pull and start all the necessary containers. 

it'll show all the containers
# docker ps -a

After that you have to checks the logs of containers to see if there are any errors if container exited or while doing api calls.

# docker logs -f $container_ID

The folder structure has been updated according to aws_be structure. Also the Dockerfiles and docker-compose file has been updated. 