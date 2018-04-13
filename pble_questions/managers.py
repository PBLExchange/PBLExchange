import os

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save, post_delete, class_prepared

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.index import Index, IndexError, EmptyIndexError, open_dir, create_in
from whoosh.qparser import QueryParser

from ckeditor_uploader.fields import RichTextUploadingField

try:
    STORAGE_DIR = settings.WHOOSH_STORAGE_DIR
except AttributeError:
    raise ImproperlyConfigured(u'Could not find WHOOSH_STORAGE_DIR setting. ' +
                               'Please make sure that you have added that setting.')

field_mapping = {
    models.AutoField: ID(unique=True, stored=True),
    models.BooleanField: STORED,
    models.CharField: TEXT,
    models.CommaSeparatedIntegerField: STORED,
    models.DateField: ID,
    models.DateTimeField: ID,
    models.DecimalField: STORED,
    models.EmailField: ID,
    models.FileField: ID,
    models.FilePathField: ID,
    models.FloatField: STORED,
    models.ImageField: ID,
    models.IntegerField: STORED,
    models.IPAddressField: ID,
    models.NullBooleanField: STORED,
    models.PositiveIntegerField: STORED,
    models.PositiveSmallIntegerField: STORED,
    models.SlugField: KEYWORD,
    models.SmallIntegerField: STORED,
    models.TextField: TEXT,
    models.TimeField: ID,
    models.URLField: ID,
    RichTextUploadingField: TEXT,
}


class WhooshManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        self.parser = None
        self.fields = kwargs.pop('fields', []) + ['id']
        self.real_time = kwargs.pop('real_time', True)
        if not os.path.lexists(STORAGE_DIR):
            os.makedirs(STORAGE_DIR)
        try:
            self.index = open_dir(STORAGE_DIR)
        except (IndexError, EmptyIndexError):
            self.index = None
        super(WhooshManager, self).__init__(*args, **kwargs)

    def contribute_to_class(self, model, name):
        super(WhooshManager, self).contribute_to_class(model, name)
        class_prepared.connect(self.class_prepared_callback, sender=self.model)

    def class_prepared_callback(self, sender, **kwargs):
        schema_dict = {}
        for field_name in self.fields:
            field = sender._meta.get_field(field_name)  # getattr(sender, field_name, None)
            if field is None:
                continue
            schema_dict.update({field.name: field_mapping[field.__class__]})
        self.schema = Schema(**schema_dict)
        if self.index is None:
            self.index = create_in(STORAGE_DIR, self.schema)  # Index(self.storage, schema=self.schema, create=True)
        self.searcher = self.index.searcher()
        if self.real_time:
            post_save.connect(self.post_save_callback, sender=self.model)
            post_delete.connect(self.post_delete_callback, sender=self.model)

    def post_save_callback(self, sender, instance, created, **kwargs):
        dct = dict([(f, str(getattr(instance, f))) for f in self.fields])
        self.index = self.index.refresh()
        writer = self.index.writer()
        if created:
            writer.add_document(**dct)
        else:
            writer.update_document(**dct)
        writer.commit()

    def post_delete_callback(self, sender, instance, **kwargs):
        pass  # TODO: add some remover function

    def query(self, q):
        if self.parser is None:
            self.parser = QueryParser(self.default, schema=self.index.schema)
        if not hasattr(self, 'searcher'):
            self.searcher = self.index.searcher()
        results = self.searcher.search(self.parser.parse(str(q)))
        return self.filter(id__in=[r['id'] for r in results])
