# Generated by Django 5.0.4 on 2024-05-07 04:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_company_consultancy_company_industry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruiters', to='reviews.company'),
        ),
    ]
