# Generated by Django 4.1.5 on 2023-04-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='group_link',
            field=models.CharField(default='https://chat.whatsapp.com/Jft58B7njSK5YHRdm0YI57', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='is_free',
            field=models.BooleanField(default=False, verbose_name='free entry'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='max_participant',
            field=models.IntegerField(blank=True, null=True, verbose_name='max participant (optional)'),
        ),
    ]
