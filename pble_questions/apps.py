from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    name = 'pble_questions'

    def ready(self):
        import pble_questions.signals
