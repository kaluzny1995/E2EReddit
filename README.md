# Reddit data engineering E2E process

A Python 3.11 application for end-to-end process automation of reddits data engineering. The solution launches: download, ingestion and popularity as well as sentiment jobs.

## Installation
Before downloading the repo you have to install [Anaconda](https://anaconda.org/). After installation clone the repo. **IMPORTANT**: The repo must be downloaded to same directory as _DownloadReddit_ and _ETLReddit_, i.e. the `ls` command must return `DownloadReddit  ETLReddit` names within the results.

Go into the downloaded repo directory.

    cd E2EReddit

Then establish new Anaconda Python 3.11 environment, like _e2e_reddit_311_ with required packages:

    conda create -n e2e_reddit_311 python=3.11 --file "requirements.txt"

Activate the Anaconda environment via: `conda activate e2e_reddit_311`. The application is now ready to be used.

## Setting up the RabbitMQ service
The RabbitMQ message queueing service is needed for setting up cronjobs via _celery_ Python package. To set it up you need first to install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) services from the provided links.

After installation create the `docker-compose.yml` file with the following content ([reference here](https://medium.com/@kaloyanmanev/how-to-run-rabbitmq-in-docker-compose-e5baccc3e644)):

```yaml
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
**NOTE**: You can set up your own default RabbitMQ username and password. By default, both are set to: _mq_admin_.
Then run command:

    docker compose up -d

Voilà. The RabbitMQ service is now set up. You can monitor logs in web browser via typing in: [http://localhost:15672/](http://localhost:15672/) and then authenticating with the provided credentials in `docker-compose.yml` file.

## Running the application
Running the help command: `python run_e2e.py -h` yields the following: 

```text
---- Reddits E2E process ----

usage: run_e2e.py [-h] phrase

Reddits E2E process Python 3.11 application.

positional arguments:
  phrase      phrase to run the E2E process for

options:
  -h, --help  show this help message and exit
```
The application run the whole E2E (_end-to-end_) process of reddits data engineering i.e.: raw data downloading, data ingestion and data ETL processing. Data visualization is handled independently directly in **Power BI** (or **Looker**) app.

### Parameters overview
1. **phrase** -- **_required_** -- word or sequence of words to run the E2E process for

**NOTE**: Currently the E2E app is implemented for: _israel_, _iran_ and _trump_ phrases. If you want to launch the app for other phrase, you need to add a task to `config.json['celery_app']['tasks']` the following section:

```json
{
  "phrase": "<your phrase>",
  "month": "month schedule",
  "day": "day schedule",
  "hour": "hour schedule",
  "minute": "minute schedule",
  "name": "<new task name>"
}
```
**NOTE**: Reference to the celery crontab schedule avalaible [here](https://docs.celeryq.dev/en/main/userguide/periodic-tasks.html).

You also have to add to `jobs.json` your new phrase subJSON like:
```json
{
  "<your new phrase>": {
    "phrase": "<your new phrase>",
    "job_type": "<JOB TYPE>",
    "command": {
      "param1": "<job param 1>",
      "param2": "<job param 2>"
    },
    "is_failed_if_error": "<should fail if command raised error?>",
    "next_jobs": ["<next job to do>"]
  }
}
```

### Launching
To launch the app you need to type in:

    python run_e2e.py "<phrase>"

Where _phrase_ denotes a word (or words) to run the E2E process for.

### Testing
To perform application unit testing simply run the command `pytest` in main project directory. The output should look like the following:
```text
================================ test session starts ================================
platform linux -- Python 3.11.15, pytest-9.0.2, pluggy-1.5.0
rootdir: /home/jakub/PycharmProjects/E2EReddit
collected 9 items                                                                                                                                                                      

test/model/test_command.py .........                                           [100%]

================================= 9 passed in 0.10s =================================
```
## Running via Celery app
To run the whole solution via Celery cronjob service run the command:

    celery -A app worker -B -l INFO

The tasks will run automatically at the scheduled time.

## E2E dataflow

![reddits_e2e_dataflow](/assets/images/reddits_e2e_dataflow.png "Reddits E2E dataflow.")

1. **DOWNLOAD job** -- raw reddit JSON files downloading and persisting them in folders
2. **INGESTION job** -- cleaning raw data from JSON files and persisting them into database
3. **POPULARITY ETL job** -- selecting popularity, processing reddit data and persisting into _popularities_ table
4. **SENTIMENT ETL job** -- selecting texts, determining their sentiment values, processing and persisting into _sentiments_ table
5. **EMOTION ETL job** -- selecting texts, determining their emotion counts, processing and persisting into _emotions_ table
6. **VECTORIZATION ETL job** -- selecting texts, converting them to vectors, processing and persisting into _vectors_ table
7. **REDUCTION ETL job** -- selecting text vectors, performing dimensionality reduction task, processing and persisting into _reductions_ table
8. **VISUALIZATION** (independent project) -- loading data from database tables and visualizing them on Power BI/Looker dashboards.

## See also

1. [Downloading reddits documentation.](https://github.com/kaluzny1995/DownloadReddit/blob/master/README.md)
2. [Reddits ingestion and ETL processes documentation.](https://github.com/kaluzny1995/ETLReddit/blob/master/README.md)
3. [Reddits visualization documentation.](https://github.com/kaluzny1995/VisReddit/blob/main/README.md)