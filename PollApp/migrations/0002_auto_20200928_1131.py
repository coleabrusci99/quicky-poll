# Generated by Django 3.1.1 on 2020-09-28 18:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('PollApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='extension',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
