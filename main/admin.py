from django.contrib import admin

from .models import OtpToken, Profile, Schedule, Route, Bus, Booking, CustomerServiceRequest, Notification, UserNotification, Communication, Feedback, Payment, RealTimeUpdates
# Register your models here.

admin.site.register(OtpToken)
admin.site.register(Profile)
admin.site.register(Schedule)
admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Route)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(UserNotification)
admin.site.register(Notification)
admin.site.register(CustomerServiceRequest)
admin.site.register(Communication)
admin.site.register(RealTimeUpdates)