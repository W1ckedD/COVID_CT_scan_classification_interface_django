# Generated by Django 4.0.1 on 2022-02-08 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='action_type',
        ),
        migrations.AddField(
            model_name='log',
            name='failure_msg',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
