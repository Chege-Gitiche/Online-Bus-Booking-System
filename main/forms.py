from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model 
from .models import Profile, Bus, Schedule, Booking , Bus, Feedback


class RegisterForm(UserCreationForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    
    
    class Meta:
        model = get_user_model()
        fields = ["username","email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Customize form fields if needed
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class BookingDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    primary_email = forms.EmailField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=255, required=False)
    payment_method = forms.ChoiceField(choices=Profile.PAYMENT_METHOD_CHOICES, required=True)


    class Meta:
        model = Profile
        fields = ['primary_email', 'phone_number', 'address', 'payment_method']

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['busNumber', 'capacity', 'type', 'status']


        


class BookingForm(forms.ModelForm):
    
    user =  forms.CharField(max_length=30, required=True)
    scheduleID =  forms.CharField(max_length=20, required=True)
    seatNumber = forms.CharField(max_length=255, required=False)
    totalPrice = forms.NumberInput(attrs={'class': 'form-control'})
        
    class Meta:
        model = Booking
        fields = ['user', 'scheduleID' , 'seatNumber', 'totalPrice']


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['busNumber', 'capacity', 'type', 'status']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments', 'suggestions']  # Include suggestions field
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'Your comments...'}),
            'suggestions': forms.Textarea(attrs={'placeholder': 'Any suggestions...'}),
        }