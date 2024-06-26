# Generated by Django 4.2 on 2024-06-08 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('bookingID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('seatNumber', models.CharField(max_length=10)),
                ('bookingDate', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='confirmed', max_length=10)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('busID', models.CharField(editable=False, max_length=20, unique=True)),
                ('busNumber', models.CharField(max_length=20)),
                ('capacity', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('Economy', 'Economy'), ('Business', 'Business')], max_length=20)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Maintenance', 'Maintenance')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField(editable=False, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('profileimg', models.ImageField(default='blank-profile-picture.png', upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routeID', models.CharField(editable=False, max_length=20, unique=True)),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('distance', models.FloatField()),
                ('fare', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='ffef80', max_length=6),
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('userNotificationID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('queued', 'Queued')], max_length=10)),
                ('message', models.TextField()),
                ('notificationDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('scheduleID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('departureTime', models.TimeField()),
                ('arrivalTime', models.TimeField()),
                ('date', models.DateField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bus')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.route')),
            ],
        ),
        migrations.CreateModel(
            name='RealTimeUpdates',
            fields=[
                ('updateID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('ontime', 'On Time'), ('delayed', 'Delayed')], max_length=10)),
                ('bookingID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('totalAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paymentMethod', models.CharField(choices=[('mpesa', 'Mpesa'), ('paypal', 'PayPal')], max_length=20)),
                ('paymentDate', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notificationID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('notificationType', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], max_length=10)),
                ('message', models.TextField()),
                ('dateSent', models.DateTimeField(auto_now_add=True)),
                ('userNotification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usernotification')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedbackID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('rating', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerServiceRequest',
            fields=[
                ('requestID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('subjectMatter', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('opened', 'Opened'), ('resolved', 'Resolved')], default='opened', max_length=10)),
                ('requestDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('communicationID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], max_length=10)),
                ('message', models.TextField()),
                ('communicationDate', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='scheduleID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.schedule'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile'),
        ),
    ]
