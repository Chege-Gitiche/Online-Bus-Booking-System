# Generated by Django 4.2 on 2024-07-02 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_customuser_role_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='8b7ceb', max_length=6),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
