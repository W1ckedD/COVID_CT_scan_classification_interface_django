# Generated by Django 4.0.1 on 2022-02-09 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_log_action_type_log_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='account_str',
            field=models.CharField(default='', max_length=100),
        ),
    ]
