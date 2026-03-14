# Reddit data engineering E2E process

A Python 3.11 application for end-to-end process automation of reddits data engineering. The solution launches: download, ingestion and popularity as well as sentiment jobs.

## Installation
Before downloading the repo you have to install [Anaconda](https://anaconda.org/). After installation clone the repo. Go into the downloaded repo directory.

    cd E2EReddit

Then establish new Anaconda Python 3.11 environment, like _e2e_reddit_311_ with required packages:

    conda create -n e2e_reddit_311 python=3.11 --file "requirements.txt"

Activate the Anaconda environment via: `conda activate e2e_reddit_311`. The application is now ready to be used.

## Setting up the RabbitMQ service
The RabbitMQ message queueing service is needed for setting up cronjobs via _celery_ Python package. To set it up you need first to install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) services from the provided links.

After installation create the `docker-compose.yml` file with the following content:

```
services:
  rabbitmq:
    image: rabbitmq:latest
    container_name: rabbitmq
    restart: always
    ports:
      - 5672:5672
      - 15672:15672
    environment:
      RABBITMQ_DEFAULT_USER: mq_admin
      RABBITMQ_DEFAULT_PASS: mq_admin
    configs:
      - source: rabbitmq-plugins
        target: /etc/rabbitmq/enabled_plugins
    volumes:
      - lib:/var/lib/rabbitmq/
      - log:/var/log/rabbitmq

configs:
  rabbitmq-plugins:
    content: "[rabbitmq_management]."  

volumes:
  lib:
    driver: local
  log:
    driver: local
```
NOTE: You can set up your own default RabbitMQ username and password. By default both are set to: _mq_admin_.
Then run command:

    docker compose up -d

Voilà. The RabbitMQ service is now set up. You can monitor logs in web browser via typing in: `localhost/15672` and then authenticating with the provided credentials in `docker-compose.yml` file.
