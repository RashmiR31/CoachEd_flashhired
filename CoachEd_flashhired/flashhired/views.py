from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request,'base.html',{})

def rechome(request):
    return render(request,'recbase.html',{})