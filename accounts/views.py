from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth

from contacts.models import Contact
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error()(request, 'Invalid login credentials')
            return redirect('login')

    return render(request,"accounts/login.html")

def register(request):
    if request.method =='POST':
        firs_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,"user already exists!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"email already used!")
                    return redirect('register')
                else:
                    user = User.objects.create_user(firs_name=firs_name, last_name=last_name, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'You are register successfully.')
        else:          
            messages.error(request,"passwords don't match")
            return redirect('register')
    else:
        return render(request,"accounts/register.html")

@login_required(login_url ='login')
def dashboard(request):

    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data ={
        'inquiries': user_inquiry,
    }
    return render(request,"accounts/dashboard.html",data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)        
        return redirect('home')
    return redirect('home')