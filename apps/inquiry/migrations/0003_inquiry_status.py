# Generated by Django 4.2.14 on 2024-07-26 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0002_alter_inquiry_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]