# Generated by Django 2.1.2 on 2018-12-23 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0014_auto_20181223_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='granthistory',
            name='ssh',
        ),
        migrations.AddField(
            model_name='granthistory',
            name='ssh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ssh.SSH'),
        ),
    ]
