# Generated by Django 5.0.4 on 2024-05-06 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0003_alter_recruiterreview_status_alter_company_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="consultancy",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="company",
            name="industry",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Tech", "Technology"),
                    ("Finance", "Finance"),
                    ("Healthcare", "Healthcare"),
                    ("Consulting", "Consulting"),
                    ("Education", "Education"),
                    ("Government", "Government"),
                    ("Retail", "Retail"),
                    ("Manufacturing", "Manufacturing"),
                    ("Other", "Other"),
                ],
                default="Other",
                max_length=255,
            ),
        ),
    ]