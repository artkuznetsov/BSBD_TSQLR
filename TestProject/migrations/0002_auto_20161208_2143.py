# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestProject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='TestPerson',
            field=models.ForeignKey(default=None, to='TestProject.TestPerson'),
        ),
        migrations.AddField(
            model_name='connectdatabase',
            name='ShadowConnectionString',
            field=models.TextField(default=None),
        ),
    ]
