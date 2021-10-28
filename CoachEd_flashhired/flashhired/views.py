from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm,CandidateForm,RecruiterForm,JobPostingForm
from django.contrib.auth import authenticate,login,logout
from .models import User,Candidate, Recruiter, JobPosting
from django.http import HttpResponse

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# Create your views here.

######################## Landing Page View #####################
def pilot(request):
    return render(request,'pilot.html',{})

def rechome(request):
    return render(request,'rechome.html',{})

######################## Registration/login and authentication section ###########
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

def logout_view(request):
    logout(request)
    return render(request,'account/logout.html')

def password_reset_request(request):
    if request.method=="POST":
        password_reset_form=PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data= password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "account/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email=render_to_string(email_template_name,c)
                    try:
                        send_mail(subject,email,'',[user.email],fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect('password_reset_done')
    password_reset_form=PasswordResetForm()

    return render(request,'account/password_reset.html',{"form":password_reset_form})

######################## Candidate Section #####################
def CandidateHome(request):
    return render(request,'candidate/CandidateHome.html')

######################## Recruiter Section #####################
 
def RecruiterHome(request):
    if request.user.is_authenticated:
        try:
            details = Recruiter.objects.get(pk=request.user)
            jobs = JobPosting.objects.all().filter(recruiter=details)
        except Recruiter.DoesNotExist:
            return HttpResponse("Create profile to continue")
        return render(request,'recruiter/RecruiterHome.html',{'details':details,'jobs':jobs})
    else:
        return HttpResponse("Login to continue")

def recruiterCreateProfile(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            print("user is authenticated")
            form = RecruiterForm(request.POST,request.FILES)
            if form.is_valid():
                print("in form valid section")
                saveInfo = form.save(commit=False) 
                saveInfo.user = request.user
                saveInfo.save()
                return redirect('RecruiterHome')             
            else:
                return HttpResponse('form not valid')
    else:
        form = RecruiterForm()
    return render(request,'recruiter/createprofile.html',{'form':form})

def recruiterProfile(request):
    if request.user.is_authenticated:
        details = Recruiter.objects.get(pk=request.user)
    return render(request,'recruiter/recruiterProfile.html',{'details':details})

def recruiterEditProfile(request):
    try:
        details = Recruiter.objects.get(pk=request.user)
    except Recruiter.DoesNotExist:
        return redirect("RecruiterHome")
    update_form = RecruiterForm(request.POST or None, instance = details)
    if update_form.is_valid():
        update_form.save()
        return redirect("recruiterProfile")
    return render(request,'recruiter/createprofile.html',{'form':update_form})

def addJob(request):
    if request.method =="POST":
        jobForm = JobPostingForm(request.POST,request.FILES)
        if jobForm.is_valid():
            saveInfo = jobForm.save(commit=False)
            recruiter = Recruiter.objects.get(pk=request.user)
            saveInfo.recruiter = recruiter
            saveInfo.save()
            return redirect("RecruiterHome")
        else:
            return HttpResponse("Form is invalid")
    else:
        jobForm = JobPostingForm()
    return render(request,'recruiter/addJob.html',{'form':jobForm})

def editJob(request,job_id):
    job_id=int(job_id)
    try:
        job_details = JobPosting.objects.get(id=job_id)
    except JobPosting.DoesNotExist:
        return redirect("RecruiterHome")
    update_jobform = JobPostingForm(request.POST or None,instance=job_details)
    if update_jobform.is_valid():
        update_jobform.save()
        return redirect("RecruiterHome")
    else:
        print("form not valid")
    return render(request,'recruiter/addJob.html',{'form':update_jobform})

def deleteJob(request,job_id):
    job_id=int(job_id)
    try:
        job_details = JobPosting.objects.get(id=job_id)
    except JobPosting.DoesNotExist:
        return redirect("RecruiterHome")
    job_details.delete()
    return redirect("RecruiterHome")