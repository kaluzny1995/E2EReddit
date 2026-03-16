import celery
from celery.schedules import crontab
import datetime as dt

import util
from model import Job

e2e_app = celery.Celery("e2e_app", broker="amqp://mq_admin:mq_admin@localhost//")


@e2e_app.on_after_configure.connect
def setup_periodic_tasks(sender: celery.Celery, **params) -> None:
    # sender.add_periodic_task(10., log_every_10_seconds.s("Celery app works."), name="celery_checkout")
    sender.add_periodic_task(
        crontab(hour=0, minute=50),
        e2e_process.s("israel"),
        name="e2e_process_israel"
    )
    sender.add_periodic_task(
        crontab(hour=1, minute=10),
        e2e_process.s("trump"),
        name="e2e_process_trump"
    )
    sender.add_periodic_task(
        crontab(hour=1, minute=30),
        e2e_process.s("iran"),
        name="e2e_process_iran"
    )


@e2e_app.task
def log_every_10_seconds(message: str) -> None:
    """ Celery app checkout message """
    print(message)


@e2e_app.task
def e2e_process(phrase: str) -> None:
    """ E2E process for given phrase """
    logger = util.setup_logger(name=f"e2e_celery_reddits_{phrase}",
                               log_file=f"logs/celery_app/e2e_reddits_{phrase}_{dt.datetime.now().isoformat()}.log")

    job = Job.from_config(phrase)
    job.run(logger=logger)
