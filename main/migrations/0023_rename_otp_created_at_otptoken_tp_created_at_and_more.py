# Generated by Django 4.2 on 2024-07-02 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_customuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otptoken',
            old_name='otp_created_at',
            new_name='tp_created_at',
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='e97d71', max_length=6),
        ),
    ]
