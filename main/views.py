from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, BookingDetailsForm
from .models import OtpToken
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Profile, Route, Schedule, Bus, Seat, Booking
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login")
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, "main/home.html", {'user_profile' : user_profile})

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

def login_user(request):
    request.session['id'] = 1
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
           login(request, user)
           
           return redirect('index')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})

def logout_user(request):
    logout(request)
    request.session['id'] = 2
    messages.success(request, ("You Were Logged Out!"))
    return redirect('home')

@login_required(login_url="/login")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        image = request.FILES.get('profile_img', user_profile.profile_img)
        
        bio = request.POST.get('bio', '')
        address = request.POST.get('address', '')
        primary_email = request.POST.get('primary_email', '')
        secondary_email = request.POST.get('secondary_email', '')
        payment_method = request.POST.get('payment_method', '')
        phone_number = request.POST.get('phone_number', '')

        user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.address = address
        user_profile.primary_email = primary_email
        user_profile.secondary_email = secondary_email
        user_profile.payment_method = payment_method
        user_profile.phone_number = phone_number
        user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url="/login")
def routes_view(request):
    routes = Route.objects.all()
    return render(request, 'routes.html', {'routes': routes})

@login_required(login_url="/login")
def search_view(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        date = request.POST.get('date')

        try:
            # Query schedules based on the selected origin, destination, and date
            schedules = Schedule.objects.filter(route__origin=origin, route__destination=destination, date=date)

            if schedules.exists():
                # Calculate total amount
                total_amount = sum(schedule.route.fare for schedule in schedules)

                # Retrieve buses associated with the schedules
                buses = [schedule.bus for schedule in schedules]

                return render(request, 'search.html', {
                    'origin': origin,
                    'destination': destination,
                    'date': date,
                    'schedules': schedules,
                    'buses': buses,
                    'total_amount': total_amount,
                    'origins': Route.objects.values_list('origin', flat=True).distinct(),
                    'destinations': Route.objects.values_list('destination', flat=True).distinct(),
                })
            else:
                message = f"No schedules found from {origin} to {destination} on {date}."
        except Exception as e:
            message = f"An error occurred: {str(e)}"

        routes = Route.objects.all()
        return render(request, 'routes.html', {'routes': routes, 'message': message})

    else:
        routes = Route.objects.all()
        return render(request, 'routes.html', {'routes': routes})

@login_required
def seat_selection_view(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    schedule = get_object_or_404(Schedule, bus=bus)
    route = schedule.route
    fare = route.fare
    
    # Fetch seats associated with the bus
    seats = Seat.objects.filter(bus=bus)
    # Organize seats into rows, assuming 4 seats per row as per your template
    seat_rows = []
    row = []
    for index, seat in enumerate(seats):
        row.append(seat)
        if (index + 1) % 4 == 0:  # Assuming 4 seats per row
            seat_rows.append(row)
            row = []
    if row:
        seat_rows.append(row)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        if selected_seats:
            selected_seats_str = ','.join(selected_seats)
            # return redirect('booking_details', selected_seats=selected_seats_str)
            return redirect("booking_details/"+str(slec))
    
    return render(request, 'seat_selection.html', {'seat_rows': seat_rows, 'bus': bus, 'fare': fare, 'origin': route.origin, 'destination': route.destination, 'total_amount': fare})

@login_required(login_url="/login/")
def booking_details(request, selected_seats):
    selected_seat_ids = selected_seats.split(',')
    selected_seat_objects = Seat.objects.filter(id__in=selected_seat_ids)
    seat_numbers = ','.join([seat.seat_number for seat in selected_seat_objects])

    user_profile = get_object_or_404(Profile, user=request.user)

    first_seat = selected_seat_objects.first()
    bus = first_seat.bus
    schedule = get_object_or_404(Schedule, bus=bus)
    route = schedule.route

    fare = route.fare
    total_amount = fare * len(selected_seat_objects)

    if request.method == 'POST':
        form = BookingDetailsForm(request.POST)
        if form.is_valid():
            booking = Booking.objects.create(
                user=request.user,
                scheduleID=schedule,
                seatNumber=seat_numbers,
                totalPrice=total_amount
            )
            return redirect('payment', booking_id=booking.id)
    else:
        initial_data = {
            'payment_method': user_profile.payment_method,
        }
        form = BookingDetailsForm(initial=initial_data)

    context = {
        'form': form,
        'selected_seats': selected_seat_objects,
        'origin': route.origin,
        'destination': route.destination,
        'departure_time': schedule.departureTime,
        'arrival_time': schedule.arrivalTime,
        'total_amount': total_amount,
        'payment_method_choices': Profile.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'booking_details.html', context)

@login_required(login_url="/login/")
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment.html', {'booking': booking})



@login_required
def lockscreen(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the desired page
        else:
            messages.error(request, 'Invalid password')
    return render(request, 'lockscreen.html')

def booking(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0114679087'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

     # Check the response status code to determine success or failure
    if response.status_code == 200:  # Adjust based on your MpesaClient implementation
        messages.success(request, "Payment request sent successfully.")
    else:
        messages.error(request, "Payment request failed.")

    # Redirect to booking.html or any other appropriate page
    return render(request, 'booking.html')  # Replace 'booking_page' with your actual URL name

