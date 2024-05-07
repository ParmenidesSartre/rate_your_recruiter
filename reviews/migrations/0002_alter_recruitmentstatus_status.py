# Generated by Django 5.0.4 on 2024-05-06 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentstatus',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Interviewed', 'Interviewed'), ('Rejected', 'Rejected'), ('Offered', 'Offered'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Withdrawn', 'Withdrawn'), ('Ghosted', 'Ghosted'), ('Other', 'Other')], max_length=20, unique=True),
        ),
    ]