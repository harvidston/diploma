# Generated by Django 3.2.18 on 2023-06-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto_20230612_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='name',
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]