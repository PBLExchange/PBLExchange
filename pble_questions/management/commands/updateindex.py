from django.core.management import BaseCommand

from pble_questions.models import Question


class Command(BaseCommand):
    help = 'Updates the Whoosh search index'

    def handle(self, *args, **options):
        for q in Question.objects.all():
            self.stdout.write('Adding question: {}'.format(q))
            Question.objects.post_save_callback(None, q, False)
