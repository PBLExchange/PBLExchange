# Celery tasks
from pble_subscriptions.models import Subscription, QuestionNotification
from pble_questions.models import Tag
from datetime import timedelta, time, date
from django.utils import timezone
from django.template import loader
from collections import defaultdict
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
# Since send_mass_email does not work with HTML message we use an alternative
from django.core.mail import get_connection, EmailMultiAlternatives

# Method for debugging---prints in the celery worker tab
# logger = get_task_logger(__name__)
# @periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
# def beat():
#    logger.info('Task executed!! DONE')


@periodic_task(run_every=(crontab(hour="07", minute="50", day_of_week="*")))
def send_daily_digest():
    midnight_today = datetime.combine(timezone.now(), time.min)
    midnight_day_ago = midnight_today - timedelta(days=1)
    q_notifications = QuestionNotification.objects.filter(created_date__gte=midnight_day_ago)
    users = Subscription.objects.filter(digest=Subscription.DAILY)
    digest_option = 'daily'  # TODO: get using subscription class macro
    category_questions = defaultdict(list)
    peer_questions = defaultdict(list)
    tag_questions = defaultdict(list)

    connection = get_connection()  # uses SMTP server specified in settings.py
    connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()

    for qn in q_notifications:
        current_users = users.exclude(user=qn.question.author)
        excl_users = []
        if qn.question.category:
            for u in current_users.filter(categories__id=qn.question.category.id):
                category_questions[u.user.username].append(qn.question)
                excl_users.append(u.user)

        # Reduce number of users to iterate
        current_users = current_users.exclude(user__in=excl_users)
        excl_users = []

        for u in current_users.filter(peers__user__id=qn.question.author.id):
            peer_questions[u.user.username].append(qn.question)
            excl_users.append(u.user)

        # Reduce number of users to iterate
        current_users = current_users.exclude(user__in=excl_users)

        for u in current_users:
            if u.tags.intersection(Tag.objects.filter(question=qn.question)):
                tag_questions[u.user.username].append(qn.question)

    # Assemble emails for the users
    for u in users:
        if category_questions[u.user.username] or peer_questions[u.user.username] or tag_questions[u.user.username]:
            u_category_questions = category_questions[u.user.username]
            u_peer_questions = peer_questions[u.user.username]
            u_tag_questions = tag_questions[u.user.username]

            html_message = loader.render_to_string(
                'subscriptions/digest_notification.html',
                {
                    'recipient': u.user.username,
                    'category_questions': u_category_questions,
                    'peer_questions': u_peer_questions,
                    'tag_questions': u_tag_questions,
                    'digest_option': digest_option
                }
            )
            message = EmailMultiAlternatives('PBL Exchange daily digest', '', 'pblexchange@aau.dk', [u.user.email],
                                             connection=connection)
            message.attach_alternative(html_message, 'text/html')
            message.send()

    connection.close()  # Cleanup


@periodic_task(run_every=(crontab(hour="*", minute="*/5", day_of_week="*")))
def send_weekly_digest():
    midnight_today = datetime.combine(date.today(), time.min)
    midnight_week_ago = midnight_today - timedelta(weeks=1)
    q_notifications = QuestionNotification.objects.filter(created_date__gte=midnight_week_ago)
    users = Subscription.objects.filter(digest=Subscription.WEEKLY)
    digest_option = 'weekly'  # TODO: get using subscription class macro
    category_questions = defaultdict(list)
    peer_questions = defaultdict(list)
    tag_questions = defaultdict(list)

    connection = get_connection()  # uses SMTP server specified in settings.py
    connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()

    for qn in q_notifications:
        current_users = users.exclude(user=qn.question.author)
        excl_users = []
        if qn.question.category:
            for u in current_users.filter(categories__id=qn.question.category.id):
                category_questions[u.user.username].append(qn.question)
                excl_users.append(u.user)

        # Reduce number of users to iterate
        current_users = current_users.exclude(user__in=excl_users)
        excl_users = []

        for u in current_users.filter(peers__user__id=qn.question.author.id):
            peer_questions[u.user.username].append(qn.question)
            excl_users.append(u.user)

        # Reduce number of users to iterate
        current_users = current_users.exclude(user__in=excl_users)

        for u in current_users:
            if u.tags.intersection(Tag.objects.filter(question=qn.question)):
                tag_questions[u.user.username].append(qn.question)

    # Assemble emails for the users
    for u in users:
        if category_questions[u.user.username] or peer_questions[u.user.username] or tag_questions[u.user.username]:
            u_category_questions = category_questions[u.user.username]
            u_peer_questions = peer_questions[u.user.username]
            u_tag_questions = tag_questions[u.user.username]

            html_message = loader.render_to_string(
                'subscriptions/digest_notification.html',
                {
                    'recipient': u.user.username,
                    'category_questions': u_category_questions,
                    'peer_questions': u_peer_questions,
                    'tag_questions': u_tag_questions,
                    'digest_option': digest_option
                }
            )
            message = EmailMultiAlternatives('PBL Exchange weekly digest', '', 'pblexchange@aau.dk', [u.user.email],
                                             connection=connection)
            message.attach_alternative(html_message, 'text/html')
            message.send()

    connection.close()  # Cleanup