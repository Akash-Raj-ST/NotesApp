# Generated by Django 3.2 on 2021-05-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210519_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file_url',
            field=models.FileField(upload_to='media/files'),
        ),
    ]
