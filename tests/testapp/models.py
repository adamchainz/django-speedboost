# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db.models import CharField, Model, TextField


class Author(Model):
    name = CharField(max_length=32, db_index=True)
    bio = TextField()

    def __unicode__(self):
        return "{} {}".format(self.id, self.name)
