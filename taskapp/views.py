from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Doctor
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


# -------- SIGNUP VIEW --------
from django.contrib.auth.hashers import make_password

def signup_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        profile_pic = request.FILES.get('profile_pic')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        hashed_password = make_password(password)

        if user_type == 'patient':
            if Patient.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect('signup')
            Patient.objects.create(
                username=username,
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                address=address,
                profile_pic=profile_pic
            )
        elif user_type == 'doctor':
            if Doctor.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect('signup')
            Doctor.objects.create(
                username=username,
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                address=address,
                profile_pic=profile_pic
            )

        messages.success(request, "Registered successfully! Please log in.")
        return redirect('login')

    return render(request, 'registration/signup.html')


# -------- LOGIN VIEW --------

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = None
        if user_type == 'patient':
            user = Patient.objects.filter(username=username).first()
        elif user_type == 'doctor':
            user = Doctor.objects.filter(username=username).first()

        # Validate user and password
        if user and check_password(password, user.password):
            request.session['username'] = user.username
            request.session['user_type'] = user_type
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials or please sign up first.")
            return redirect('login')

    return render(request, 'registration/login.html')

# -------- DASHBOARD VIEW --------
def dashboard_view(request):
    username = request.session.get('username')
    user_type = request.session.get('user_type')

    if not username or not user_type:
        return redirect('login')

    user = None
    if user_type == 'patient':
        try:
            user = Patient.objects.get(username=username)
        except Patient.DoesNotExist:
            return redirect('login')
    elif user_type == 'doctor':
        try:
            user = Doctor.objects.get(username=username)
        except Doctor.DoesNotExist:
            return redirect('login')

    return render(request, 'dashboard.html', {
        'user': user,
        'user_type': user_type,
    })


# -------- LOGOUT VIEW --------
def logout_view(request):
    request.session.flush()
    return redirect('login')
