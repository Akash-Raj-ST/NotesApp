# Generated by Django 3.2 on 2021-05-16 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='box',
            fields=[
                ('sect_box_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('box_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='section',
            fields=[
                ('section_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('section_name', models.CharField(max_length=25)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('file_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=250)),
                ('file_url', models.CharField(max_length=100)),
                ('sect_box_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.box')),
            ],
        ),
        migrations.AddField(
            model_name='box',
            name='section_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.section'),
        ),
    ]
