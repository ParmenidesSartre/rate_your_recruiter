# Generated by Django 5.0.4 on 2024-05-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_alter_recruitmentstatus_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruiterreview",
            name="status",
            field=models.CharField(
                choices=[
                    ("Applied", "Applied"),
                    ("Interviewed", "Interviewed"),
                    ("Rejected", "Rejected"),
                    ("Offered", "Offered"),
                    ("Accepted", "Accepted"),
                    ("Declined", "Declined"),
                    ("Withdrawn", "Withdrawn"),
                    ("Ghosted", "Ghosted"),
                    ("Other", "Other"),
                ],
                default="Applied",
                help_text="Current status of the recruitment process.",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
        migrations.DeleteModel(
            name="RecruitmentStatus",
        ),
    ]