# Celery tasks
from celery import Celery

#app = Celery('tasks', broker='amqp://guest@localhost//')


from celery.schedules import crontab
from celery.task import periodic_task
#from myapp.utils import scrapers
from celery.utils.log import get_task_logger
from datetime import datetime
from django.core.mail import send_mail

logger = get_task_logger(__name__)
from PBLExchangeDjango.celery import app as celery_app


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_example():
    logger.info("Start task")
    #now = datetime.now()
    #result = scrapers.scraper_example(now.day, now.minute)
    logger.info("Task finished: result = blabla")


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def email_task():
    send_mail('Periodic task', 'A minute passed since last job execution', 'GideonBlegmand@gmail.com', ['Gblegm13@student.aau.dk'], fail_silently=False)
