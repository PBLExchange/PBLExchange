from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import connections

from pble_questions.models import Category, Question, Tag, Answer, Comment, QuestionVote, AnswerVote
from pble_subscriptions.models import Subscription
from pble_users.models import UserProfile, UserSetting


class Command(BaseCommand):
    help = 'Transfer Q2A database to internal database'
    __user_lookup = {}
    __category_lookup = {}
    __post_lookup = {}

    def handle(self, *args, **options):
        with connections['transferfrom'].cursor() as cursor:
            self.handle_users(cursor)
            self.handle_categories(cursor)
            self.handle_posts(cursor)
            self.handle_votes(cursor)

    def handle_users(self, cursor):
        self.stdout.write('Transferring users...')
        cursor.execute('''
            SELECT qa_users.userid, email, handle, COALESCE(points, 0)
            FROM qa_users NATURAL LEFT OUTER JOIN qa_userpoints;
        ''')
        UserModel = get_user_model()
        for row in cursor.fetchall():
            if row[3] < 1:
                continue
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: row[2],
                'email': row[1]
            })
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.points = row[3]
            profile.save()
            settings, created = UserSetting.objects.get_or_create(user=user)
            settings.save()
            subscriptions, created = Subscription.objects.get_or_create(user=user)
            subscriptions.save()
            if row[0] not in self.__user_lookup.keys():
                self.__user_lookup.update({row[0]: user})
        self.stdout.write('Finished transferring users...')

    def handle_categories(self, cursor):
        self.stdout.write('Transferring categories...')
        cursor.execute('''
            SELECT categoryid, title, content
            FROM qa_categories;
        ''')

        for row in cursor.fetchall():
            category, created = Category.objects.get_or_create(
                da_name=str(row[1]),
                da_description=str(row[2]),
                en_name=str(row[1]),
                en_description=''
            )
            category.save()

            if row[0] not in self.__category_lookup.keys():
                self.__category_lookup.update({row[0]: category})

        self.stdout.write('Finished transferring categories...')

    def handle_posts(self, cursor):
        self.stdout.write('Transferring posts...')
        cursor.execute('''
            SELECT type, userid, title, content, created, tags, anonymous, postid, parentid, categoryid
            FROM qa_posts
        ''')

        for row in cursor.fetchall():
            # self.stdout.write('Testing on {}'.format(row[2]))
            if not row[1]:
                self.stdout.write('Skipping post: {}'.format(row[2]))
                continue
            if row[0] == 'Q':
                p, created = Question.objects.get_or_create(
                    title=str(row[2]),
                    body=str(row[3]),
                    author=self.__user_lookup[row[1]],
                    anonymous=False if row[6] == '0' else True)
                #self.stdout.write(p.title)
                p.category = self.__category_lookup[row[9]]
            elif row[0] == 'A':
                try:
                    q = self.__post_lookup[row[8]]
                except KeyError:
                    continue
                p, created = Answer.objects.get_or_create(
                    question=self.__post_lookup[row[8]],
                    body=str(row[3]),
                    author=self.__user_lookup[row[1]],
                    anonymous=False if row[6] == '0' else True
                )
            elif row[0] == 'C':
                try:
                    q = self.__post_lookup[row[8]].question
                    a = self.__post_lookup[row[8]]
                except KeyError:
                    continue
                if not (q or a):
                    continue
                p, created = Comment.objects.get_or_create(
                    question=q,
                    answer=a,
                    body=str(row[3]),
                    author=self.__user_lookup[row[1]],
                    anonymous=False if row[6] == '0' else True
                )
            p.save()
            if row[7] not in self.__post_lookup.keys():
                self.__post_lookup.update({row[7]: p})

        self.stdout.write('Finished transferring posts...')

    def handle_votes(self, cursor):
        self.stdout.write('Transferring votes...')
        cursor.execute('''
            SELECT postid, userid, vote
            FROM qa_uservotes
        ''')

        for row in cursor.fetchall():
            try:
                post = self.__post_lookup[row[0]]
                user = self.__user_lookup[row[1]]
            except KeyError:
                continue

            if isinstance(post, Question):
                QuestionVote.objects.get_or_create(
                    post=post,
                    user=user,
                    vote=row[2]
                )
            elif isinstance(post, Answer):
                AnswerVote.objects.get_or_create(
                    post=post,
                    user=user,
                    vote=row[2]
                )

        self.stdout.write('Finished transferring votes...')
