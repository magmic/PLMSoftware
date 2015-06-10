# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SRMapp', '0004_auto_20150518_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
