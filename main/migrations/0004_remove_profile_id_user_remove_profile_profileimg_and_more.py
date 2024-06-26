# Generated by Django 4.2 on 2024-06-17 15:15

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_booking_bus_profile_route_alter_otptoken_otp_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profileimg',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('mpesa', 'Mpesa'), ('paypal', 'PayPal')], max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='primary_email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='secondary_email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='686f83', max_length=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='US'),
        ),
    ]
