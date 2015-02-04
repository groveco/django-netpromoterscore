# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('netpromoterscore', '0002_promoterscore_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promoterscore',
            name='score',
            field=models.IntegerField(default=-1, validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(10)]),
            preserve_default=True,
        ),
    ]
