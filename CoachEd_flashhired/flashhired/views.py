from django.shortcuts import render


# Create your views here.

def pilot(request):
    return render(request,'pilot.html',{})

def rechome(request):
    return render(request,'rechome.html',{})

def login(request):
    return render(request,'login.html',{})

def SignupChoice(request):
    return render(request,'SignupChoice.html',{})


def Signup(request):
    return render(request,'Signup.html',{})