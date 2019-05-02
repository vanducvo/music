# Generated by Django 2.2 on 2019-04-29 18:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_remove_song_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio',
            field=models.FileField(default=django.utils.timezone.now, upload_to='songs/'),
            preserve_default=False,
        ),
    ]
