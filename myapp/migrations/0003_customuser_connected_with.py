# Generated by Django 4.2.1 on 2023-05-11 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_customuser_email_remove_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='connected_with',
            field=models.CharField(default='', max_length=255),
        ),
    ]
