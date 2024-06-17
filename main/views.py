from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Profile

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login")
def index(request):
    return render(request, "main/home.html")

def home(request):
    return render(request,'main/base.html')


def signUp(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('verify-email',username=request.POST['username'])
    else:
        form = RegisterForm()
    
    return render(request,'registration/sign_up.html',{"form":form})


def verifyEmail(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("login")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)


def resendOtp(request):
    
    if request.method == 'POST':
        
                user_email = request.POST["otp_email"]
                
                if get_user_model().objects.filter(email=user_email).exists():
                    user = get_user_model().objects.get(email=user_email)
                    otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
                    
                    
                    # email variables
                    subject="Email Verification"
                    message = f"""
                                        Hi {user.username}, here is your OTP {otp.otp_code} 
                                        it expires in 5 minute, use the url below to redirect back to the website
                                        http://127.0.0.1:8000/verify-email/{user.username}
                                        
                                        """
                    sender = "chegegitiche254@gmail.com"
                    receiver = [user.email, ]
                
                
                    # send email
                    send_mail(
                            subject,
                            message,
                            sender,
                            receiver,
                            fail_silently=False,
                        )
                    
                    messages.success(request, "A new OTP has been sent to your email-address")
                    return redirect("verify-email", username=user.username)

                else:
                    messages.warning(request, "This email dosen't exist in the database")
                    return redirect("resend-otp")
       
           
    context = {}
    return render(request, "resend_otp.html", context)



def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect("index")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    return render(request, "login.html")

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Authentication failed
                # Handle error or display message
                pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



@login_required(login_url="/login")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
        else:
            image = request.FILES.get('image')

        bio = request.POST.get('bio', '')
        address = request.POST.get('address', '')
        primary_email = request.POST.get('primary_email', '')
        secondary_email = request.POST.get('secondary_email', '')
        payment_method = request.POST.get('payment_method', '')

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.address = address
        user_profile.primary_email = primary_email
        user_profile.secondary_email = secondary_email
        user_profile.payment_method = payment_method
        user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

