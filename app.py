import celery
from celery.schedules import crontab
import datetime as dt

import util
from model import CeleryAppConfig, Job

config = CeleryAppConfig.from_config()
e2e_app = celery.Celery(config.name, broker=config.get_rabbitmq_broker_string())


@e2e_app.on_after_configure.connect
def setup_periodic_tasks(sender: celery.Celery, **params) -> None:
    # sender.add_periodic_task(crontab(minute="*/10", hour="*"), log_message.s("Celery app works. 10 mins checkout."), name="celery_10mins_checkout")
    for task in config.tasks:
        sender.add_periodic_task(
            crontab(hour=util.to_utc(task.hour), minute=task.minute, day_of_month=task.day, month_of_year=task.month),
            e2e_process.s(task.phrase),
            name=task.name
        )


@e2e_app.task
def log_message(message: str) -> None:
    """ Celery app checkout message """
    print(message)


@e2e_app.task
def e2e_process(phrase: str) -> None:
    """ E2E process for given phrase """
    logger = util.setup_logger(name=f"e2e_celery_reddits_{phrase}",
                               log_file=f"logs/celery_app/e2e_reddits_{phrase}_{dt.datetime.now().isoformat()}.log")

    job = Job.from_config(phrase)
    job.run(logger=logger)
