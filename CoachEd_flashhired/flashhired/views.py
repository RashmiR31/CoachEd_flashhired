from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.http import HttpResponse
# Create your views here.

def pilot(request):
    return render(request,'pilot.html',{})

def rechome(request):
    return render(request,'rechome.html',{})

def login_view(request):
    msg=None
    form = LoginForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_candidate:
                login(request,user)
                return redirect('CandidateHome')
            if user is not None and user.is_recruiter:
                login(request,user)
                return redirect('RecruiterHome')
            else:
                msg='invalid credentials'
                print(msg)
        else:
            msg='error validating form'
    return render(request,'account/login.html',{'form':form,'msg':msg})

def SignupChoice(request):
    return render(request,'account/SignupChoice.html',{})

def candidateSignup(request):
    msg=None
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg='user created successfully'
            return redirect('login_view')
        else: 
            msg='form is not valid'
    else: 
        form = SignupForm() 
    return render(request,'account/candidatesignup.html',{'form':form,'msg':msg})

def recruiterSignup(request):
    msg=None
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg='user created successfully'
            return redirect('login_view')
        else: 
            msg='form is not valid'
    else: 
        form = SignupForm() 
    return render(request,'account/recruiterSignup.html',{'form':form,'msg':msg})

def home(request):
    return render(request,'home.html')

def CandidateHome(request):
    return render(request,'CandidateHome.html')
    
def RecruiterHome(request):
    return render(request,'RecruiterHome.html')

def logout_view(request):
    logout(request)
    return render(request,'account/logout.html')