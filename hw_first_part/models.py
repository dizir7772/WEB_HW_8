"""
Створіть хмарну базу даних Atlas MongoDB

За допомогою ODM Mongoengine створіть моделі для зберігання даних із цих файлів у колекціях authors та quotes.
Під час зберігання цитат (quotes), поле автора в документі повинно бути не рядковим значенням,
а Reference fields полем, де зберігається ObjectID з колекції authors.
"""

from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    quote = StringField()
    author = ReferenceField(Authors, dbref=False, reverse_delete_rule=CASCADE)
    meta = {'allow_inheritance': True}
