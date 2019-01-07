# Generated by Django 2.1.2 on 2018-12-23 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0011_auto_20181121_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrantHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.TextField(default='', max_length=1000)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
