# Generated by Django 4.0.1 on 2022-02-08 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_remove_log_action_type_log_failure_msg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='failure_msg',
        ),
    ]
