# Generated by Django 5.1.5 on 2025-03-01 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_adimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='Email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='ad',
            name='contact',
            field=models.IntegerField(null=True),
        ),
    ]
