# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SRMapp', '0003_auto_20150518_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='surv_delivery_time',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplier',
            name='surv_price',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplier',
            name='surv_quality',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2),
            preserve_default=True,
        ),
    ]
