# Generated by Django 2.2.3 on 2019-08-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0002_auto_20190817_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='video_episode',
            name='episodeMd5',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]