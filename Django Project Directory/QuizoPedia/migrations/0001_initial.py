# Generated by Django 4.1 on 2022-08-09 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCredential',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('userEmail', models.CharField(max_length=40)),
                ('userPassword', models.CharField(max_length=20)),
            ],
        ),
    ]
