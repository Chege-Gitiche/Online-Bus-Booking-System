from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



class OtpToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images/', default='blank-profile-picture.png')
    address = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    primary_email = models.EmailField(max_length=255, blank=True)
    secondary_email = models.EmailField(max_length=255, blank=True)
    PAYMENT_METHOD_CHOICES = (
        ('mpesa', 'Mpesa'),
        ('paypal', 'PayPal'),
    )
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, blank=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)  

    def __str__(self):
        return self.user.username
    
# Bus Model
class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Maintenance', 'Maintenance'),
    ]

    busNumber = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.busNumber

    def create_seats(self):
        for seat_number in range(1, (self.capacity + 1)):
            Seat.objects.create(bus=self, seat_number=str(seat_number).zfill(2))

# Seats Model
class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def _str_(self):
        return f"Seat {self.seat_number} on {self.bus.name}"

# Route Model
class Route(models.Model):
    routeID = models.CharField(max_length=20, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.FloatField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.origin} to {self.destination}'

# Schedule Model
class Schedule(models.Model):
    scheduleID = models.AutoField(primary_key=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departureTime = models.TimeField()
    arrivalTime = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f'Schedule {self.scheduleID} for Bus {self.bus.busNumber}'

    
# Booking model
class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    scheduleID = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seatNumber = models.CharField(max_length=255)
    bookingDate = models.DateTimeField(auto_now_add=True)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.bookingID} for {self.user} on {self.scheduleID}"

# Payment model
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'Mpesa'),
        ('paypal', 'PayPal'),
    ]

    paymentID = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentMethod = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    paymentDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.paymentID}'

# Feedback model
class Feedback(models.Model):
    feedbackID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback {self.feedbackID}'
# UserNotifications model
class UserNotification(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('queued', 'Queued'),
    ]

    userNotificationID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.TextField()
    notificationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification {self.userNotificationID}'

# Notification model
class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    notificationID = models.AutoField(primary_key=True)
    userNotification = models.ForeignKey(UserNotification, on_delete=models.CASCADE)
    notificationType = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    dateSent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification {self.notificationID}'

# Customer Service Requests model
class CustomerServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('opened', 'Opened'),
        ('resolved', 'Resolved'),
    ]

    requestID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subjectMatter = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='opened')
    requestDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request {self.requestID}'

# Communication model
class Communication(models.Model):
    COMMUNICATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    communicationID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=COMMUNICATION_TYPE_CHOICES)
    message = models.TextField()
    communicationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Communication {self.communicationID}'
    
# Realtime Updates
class RealTimeUpdates(models.Model):
    STATUS_CHOICES = [
        ('ontime', 'On Time'),
        ('delayed', 'Delayed'),
    ]

    updateID = models.AutoField(primary_key=True)
    bookingID = models.ForeignKey(Booking, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f'RealTimeUpdate {self.updateID}'




    

