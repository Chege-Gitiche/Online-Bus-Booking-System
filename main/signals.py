#signals.py
from django.db.models.signals import post_save,  pre_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile, Bus, Seat, Booking,Schedule

user = get_user_model()
 
@receiver(post_save, sender=User) 
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        
        else:
            OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active=False 
            instance.save()
        
        
        # setting email credentials
        otp = OtpToken.objects.filter(user=instance).last()
       
       
        subject="Email Verification"
        message = f"""
                                Hi {instance.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{instance.username}
                                
                                """
        sender = "chegegitiche254@gmail.com"
        receiver = [instance.email, ]
       
        
        
        # send email
        send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

@receiver(post_save, sender=User,dispatch_uid='save_new_user_profile')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Bus, dispatch_uid='create_seats_for_bus')
def create_seats(sender, instance, created, **kwargs):
    if created:
        instance.create_seats()


@receiver(pre_save, sender=Bus, dispatch_uid='alert users of bus')
def bus_status_change(sender, instance, **kwargs):
    if instance.busNumber:
        old_bus = Bus.objects.get(busNumber=instance.busNumber)
        if old_bus.status == 'Active' and instance.status == 'Maintenance':
            # Fetch all bookings for this bus
            bookings = Booking.objects.filter(scheduleID__bus=instance)
            for booking in bookings:
                user_profile = booking.user
                # Send notification
                send_bus_maintenance_notification(user_profile, instance)

def send_bus_maintenance_notification(user_profile, bus):
        subject="Bus change notification"
        message = f"""
        Dear {user_profile.user.username},
        
        We regret to inform you that the bus you were scheduled to board {bus.busNumber} is now under maintenance.
        We will provide an email briefly on the new bus that will be assigned to you.

        Best regards,
        Basi Bus Team
        """

        sender = "chegegitiche254@gmail.com"
        receiver = [user_profile.user.email]


        send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
        )
        

@receiver(pre_save, sender=Schedule)
def schedule_bus_change(sender, instance, **kwargs):
    if instance.pk:
        old_schedule = Schedule.objects.get(pk=instance.pk)
        if old_schedule.bus != instance.bus:
            # Fetch all bookings for this schedule
            bookings = Booking.objects.filter(scheduleID=instance)
            for booking in bookings:
                user_profile = booking.user
                # Send notification
                send_bus_change_notification(user_profile, old_schedule.bus, instance.bus, instance)

def send_bus_change_notification(user_profile, old_bus, new_bus, schedule):
    subject="Bus Reallocation notification"
    message = f"""
    Dear {user_profile.user.username},
    
    We would like to inform you that the bus for your scheduled trip (Schedule ID: {schedule.scheduleID}) has been changed.
    
    Old Bus: {old_bus.busNumber}
    New Bus: {new_bus.busNumber}
    
    Please contact our support team if you have any questions or concerns.
    
    Best regards,
    Basi Bus Team
    """

    sender = "chegegitiche254@gmail.com"
    receiver = [user_profile.user.email]
    
    send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
    )
  