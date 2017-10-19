from django.db import models


# Create your models here.
class MenuField:
    def __init__(self, title, lookup):
        self.title = title
        self.lookup = lookup


class Menu:
    fields = []

    @classmethod
    def register(cls, title, lookup):
        cls.fields.append(MenuField(title, lookup))
