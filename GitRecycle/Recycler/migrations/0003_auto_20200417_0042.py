# Generated by Django 2.2.9 on 2020-04-17 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recycler', '0002_auto_20200417_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo',
            name='create_date',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
