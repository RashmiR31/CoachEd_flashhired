from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from .models import User,Candidate, Recruiter, JobPosting
from django.http import HttpResponse
import os
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
    if request.user.is_authenticated and request.user.is_candidate:
        try:
            details = Candidate.objects.get(pk=request.user)
        except Candidate.DoesNotExist:
            return HttpResponse("Create profile to continue")
        return render(request,'candidate/CandidateHome.html',{'details':details})
    else:
        return HttpResponse("Login as Candidate to continue")

def candidateCreateProfile(request):
    if request.method=="POST":
        form=CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            print("inside form valid")
            saveInfo=form.save(commit=False)
            saveInfo.user=request.user
            saveInfo.save()
            return redirect('CandidateHome')
        else:
            return HttpResponse("Form is not valid")
    else:
        form=CandidateForm()
    return render(request,'candidate/createprofile.html',{'form':form})

def candidateProfile(request):
    if request.user.is_authenticated:
        details = Candidate.objects.get(pk=request.user)
        exp_details = Experience.objects.all().filter(candidate=details)
        acc_details = Accomplishments.objects.all().filter(candidate=details)
        project_details = Projects.objects.all().filter(candidate=details)
        skill_details = Skills.objects.all().filter(candidate=details)
        language_details = Languages.objects.all().filter(candidate=details)
        social_links = SocialLinks.objects.all().filter(candidate=details)
    context={
        'details':details,
        'exp_details':exp_details,
        'acc_details':acc_details,
        'project_details':project_details,
        'skill_details':skill_details,
        'language_details':language_details,
        'social_links':social_links,
    }
    return render(request,'candidate/candidateProfile.html',context)

def candidateEditProfile(request):
    try:
        details = Candidate.objects.get(pk=request.user)
    except Candidate.DoesNotExist:
        return redirect("CandidateHome")
    update_form = CandidateForm(request.POST or None, instance = details)
    if update_form.is_valid():
        if len(request.FILES) != 0:
            if len(request.FILES['profile_pic']) > 0:
                os.remove(details.profile_pic.path)
            details.profile_pic = request.FILES['profile_pic']
            # if len(request.FILES['recent_marks_card']) > 0:
            #     os.remove(details.recent_marks_card.path)
            # details.recent_marks_card = request.FILES['recent_marks_card']
       
            # if len(details.pu_marks_card) > 0:
            #     os.remove(details.pu_marks_card.path)
            # details.pu_marks_card = request.FILES['pu_marks_card']
        
            # if len(details.tenth_marks_card) > 0 :
            #     os.remove(details.tenth_marks_card.path)
            # details.tenth_marks_card = request.FILES['tenth_marks_card']
        update_form.save()
        return redirect("candidateProfile")
    return render(request,'candidate/createprofile.html',{'form':update_form})

############### PROJECTS ##################
def candidateProjects(request):
    if request.method=="POST":
        projects_form = CandidateProjectsForm(request.POST,request.FILES)
        if projects_form.is_valid():
            saveInfo=projects_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            saveInfo.candidate = candidate
            saveInfo.save()
            return redirect('candidateProfile')
        else:
            return HttpResponse("Form not valid")
    else:
        projects_form = CandidateProjectsForm()
    return render(request,'candidate/projects.html',{'form':projects_form})

def editProjects(request,project_id):
    project_id=int(project_id)
    try:
        project_details = Projects.objects.get(id=project_id)
    except Projects.DoesNotExist:
        return redirect("candidateProfile")
    update_projectform = CandidateProjectsForm(request.POST or None,instance=project_details)
    if update_projectform.is_valid():
        update_projectform.save()
        return redirect("candidateProfile")
    else:
        print("form not valid")
    return render(request,'candidate/projects.html',{'form':update_projectform})

def deleteProjects(request,project_id):
    project_id=int(project_id)
    try:
        project_details = Projects.objects.get(id=project_id)
    except Projects.DoesNotExist:
        return redirect("candidateProfile")
    project_details.delete()
    return redirect("candidateProfile")

######## ACCOMPLISHMENTS ###############

def candidateAccomplishments(request):
    if request.method=="POST":
        acc_form = CandidateAccomplishmentsForm(request.POST,request.FILES)
        if acc_form.is_valid():
            saveInfo=acc_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            saveInfo.candidate = candidate
            saveInfo.save()
            return redirect('candidateProfile')
        else:
            return HttpResponse("Form not valid")
    else:
        acc_form = CandidateAccomplishmentsForm()
    return render(request,'candidate/accomplishments.html',{'form':acc_form})

def editAccomplishments(request,acc_id):
    acc_id=int(acc_id)
    try:
        acc_details = Accomplishments.objects.get(id=acc_id)
    except Accomplishments.DoesNotExist:
        return redirect("candidateProfile")
    update_accform = CandidateAccomplishmentsForm(request.POST or None,instance=acc_details)
    if update_accform.is_valid():
        print("inside form valid")
        if len(request.FILES) != 0:
            if len(acc_details.certificate_doc) > 0:
                print("inside cert_doc>0")
                os.remove(acc_details.certificate_doc.path)
            acc_details.upload_doc = request.FILES['certificate_doc']
        update_accform.save()
        return redirect("candidateProfile")
    else:
        print("form not valid")
    return render(request,'candidate/accomplishments.html',{'form':update_accform})

def deleteAccomplishments(request,acc_id):
    acc_id=int(acc_id)
    try:
        acc_details = Accomplishments.objects.get(id=acc_id)
    except Accomplishments.DoesNotExist:
        return redirect("candidateProfile")
    if len(acc_details.certificate_doc)>0:
        os.remove(acc_details.certificate_doc.path)
    acc_details.delete()
    return redirect("candidateProfile")
######## CANDIDATE WORK EXPERIENCE ###############
def candidateExperience(request):
    if request.method=="POST":
        exp_form = CandidateExperienceForm(request.POST,request.FILES)
        if exp_form.is_valid():
            saveInfo=exp_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            saveInfo.candidate = candidate
            saveInfo.save()
            return redirect('candidateProfile')
        else:
            return HttpResponse("Form not valid")
    else:
        exp_form = CandidateExperienceForm()
    return render(request,'candidate/experience.html',{'form':exp_form})

def editExperience(request,exp_id):
    exp_id=int(exp_id)
    try:
        exp_details = Experience.objects.get(id=exp_id)
    except Experience.DoesNotExist:
        return redirect("candidateProfile")
    update_expform = CandidateExperienceForm(request.POST or None,instance=exp_details)
    if update_expform.is_valid():
        update_expform.save()
        return redirect("candidateProfile")
    else:
        print("form not valid")
    return render(request,'candidate/experience.html',{'form':update_expform})

def deleteExperience(request,exp_id):
    exp_id=int(exp_id)
    try:
        exp_details = Experience.objects.get(id=exp_id)
    except Experience.DoesNotExist:
        return redirect("candidateProfile")
    exp_details.delete()
    return redirect("candidateProfile")

############## CANDIDATE SKILLS ##############
def candidateSkills(request):
    if request.method=="POST":
        skill_form = CandidateSkillsForm(request.POST,request.FILES)
        if skill_form.is_valid():
            saveInfo=skill_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            saveInfo.candidate = candidate
            saveInfo.save()
            return redirect('candidateProfile')
        else:
            return HttpResponse("Form not valid")
    else:
        skill_form = CandidateSkillsForm()
    return render(request,'candidate/skills.html',{'form':skill_form})

def editSkills(request,skill_id):
    skill_id=int(skill_id)
    try:
        skill_details = Skills.objects.get(id=skill_id)
    except Skills.DoesNotExist:
        return redirect("candidateProfile")
    update_skillform = CandidateSkillsForm(request.POST or None,instance=skill_details)
    if update_skillform.is_valid():
        if len(request.FILES) != 0:
            if len(skill_details.supporting_doc)>0:
                os.remove(skill_details.supporting_doc.path)
            skill_details.supporting_doc = request.FILES['supporting_doc']
        update_skillform.save()
        return redirect("candidateProfile")
    else:
        print("form not valid")
    return render(request,'candidate/skills.html',{'form':update_skillform})

def deleteSkills(request,skill_id):
    skill_id=int(skill_id)
    try:
        skill_details = Skills.objects.get(id=skill_id)
    except Skills.DoesNotExist:
        return redirect("candidateProfile")
    if len(skill_details.supporting_doc)>0:
        os.remove(skill_details.supporting_doc.path)
    skill_details.delete()
    return redirect("candidateProfile")
############ CANDIDATE LANGUAGES KNOWN ################
def candidateLanguages(request):
    if request.method=="POST":
        lan_form = CandidateLanguagesForm(request.POST,request.FILES)
        if lan_form.is_valid():
            saveInfo=lan_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            saveInfo.candidate = candidate
            saveInfo.save()
            return redirect('candidateProfile')
        else:
            return HttpResponse("Form not valid")
    else:
        lan_form = CandidateLanguagesForm()
    return render(request,'candidate/languages.html',{'form':lan_form})

def editLanguages(request,lan_id):
    lan_id=int(lan_id)
    try:
        lan_details = Languages.objects.get(id=lan_id)
    except Languages.DoesNotExist:
        return redirect("candidateProfile")
    update_lanform = CandidateLanguagesForm(request.POST or None,instance=lan_details)
    if update_lanform.is_valid():
        update_lanform.save()
        return redirect("candidateProfile")
    else:
        print("form not valid")
    return render(request,'candidate/languages.html',{'form':update_lanform})

def deleteLanguages(request,lan_id):
    lan_id=int(lan_id)
    try:
        lan_details = Languages.objects.get(id=lan_id)
    except Languages.DoesNotExist:
        return redirect("candidateProfile")
    lan_details.delete()
    return redirect("candidateProfile")
############## CANDIDATE SOCIAL HANDLES ###############
def candidateSocialLinks(request):
    if request.method=="POST":
        sl_form = CandidateSocialLinksForm(request.POST,request.FILES)
        if sl_form.is_valid():
            saveInfo=sl_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            saveInfo.candidate = candidate
            saveInfo.save()
            return redirect('candidateProfile')
        else:
            return HttpResponse("Form not valid")
    else:
        sl_form = CandidateSocialLinksForm()
    return render(request,'candidate/sociallinks.html',{'form':sl_form})

def editSocialLinks(request,sl_id):
    sl_id=int(sl_id)
    try:
        sl_details = SocialLinks.objects.get(id=sl_id)
    except SocialLinks.DoesNotExist:
        return redirect("candidateProfile")
    update_slform = CandidateSocialLinksForm(request.POST or None,instance=sl_details)
    if update_slform.is_valid():
        update_slform.save()
        return redirect("candidateProfile")
    else:
        print("form not valid")
    return render(request,'candidate/sociallinks.html',{'form':update_slform})

########## JOB PORTAL ###############
def candidateJobPortal(request):
    if request.user.is_authenticated and request.user.is_candidate:
        try:
            job_details = JobPosting.objects.all()
        except JobPosting.DoesNotExist:
            return redirect("candidateHome")
    return render(request,'candidate/candidatejobportal.html',{'job_details':job_details})

def candidateViewJob(request,job_id):
    job_id=int(job_id)
    if request.user.is_authenticated and request.user.is_candidate:
        try:
            job_details = JobPosting.objects.get(id=job_id)
            applied_to_job_details = JobApplication.objects.all()
            candidate = Candidate.objects.get(pk=request.user)
            job = JobPosting.objects.get(id=job_id)
            try:
                if JobApplication.objects.get(candidate=candidate,job=job):
                    print("applied")
                    applied = True
            except JobApplication.DoesNotExist:
                print("not applied")
                applied = False
        except JobPosting.DoesNotExist:
            return redirect('candidateJobPortal')
    return render(request,'candidate/candidateviewjob.html',{'job_details':job_details,'applied':applied})

def candidateJobApplication(request,job_id):
    job_id = int(job_id)
    try: 
        candidate = Candidate.objects.get(pk=request.user)
        if JobApplication.objects.get(candidate=candidate,job=job_id):
            applied=True
    except JobApplication.DoesNotExist:
        print("not applied")
        applied = False
    if request.method=="POST" and request.user.is_candidate:
        apply_form = JobApplicationForm(request.POST)
        if apply_form.is_valid():
            print("inside application form valid")
            saveInfo = apply_form.save(commit=False)
            candidate = Candidate.objects.get(pk=request.user)
            job = JobPosting.objects.get(id=job_id)
            saveInfo.candidate = candidate
            saveInfo.job = job
            saveInfo.status = "Applied"
            saveInfo.save()
            return redirect('candidateViewJob',job_id)
        else:
            return HttpResponse("application form not valid")
    else:
        apply_form= JobApplicationForm()
    current_job = JobPosting.objects.get(id=job_id)
    return render(request,'candidate/jobapplication.html',{'apply_form':apply_form,'applied':applied,'job':current_job})
        
    

######################## Recruiter Section #####################
 
def RecruiterHome(request):
    if request.user.is_authenticated and request.user.is_recruiter:
        try:
            details = Recruiter.objects.get(pk=request.user)
            jobs = JobPosting.objects.all().filter(recruiter=details)
        except Recruiter.DoesNotExist:
            return HttpResponse("Create profile to continue")
        return render(request,'recruiter/RecruiterHome.html',{'details':details,'jobs':jobs})
    else:
        return HttpResponse("Login as recruiter to continue")


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
        if len(request.FILES) != 0:
            if len(details.profile_pic) > 0:
                os.remove(details.profile_pic.path)
            details.profile_pic = request.FILES['profile_pic']
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
        if len(request.FILES) != 0:
            if len(job_details.upload_doc) > 0:
                os.remove(job_details.upload_doc.path)
            job_details.upload_doc = request.FILES['upload_doc']
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
    if len(job_details.upload_doc)>0:
        os.remove(job_details.upload_doc.path)
    job_details.delete()
    return redirect("RecruiterHome")

def viewJob(request,job_id):
    job_id = int(job_id)
    try:
        job_details = JobPosting.objects.get(id=job_id)
        try:
            candidate_ids = JobApplication.objects.all().filter(job=job_id).values('candidate')
            print(candidate_ids)
            applicants=[]
            for value in candidate_ids:
                c_id=value['candidate']
                applicants.append(Candidate.objects.get(user_id=c_id))
            print(applicants)
        except JobApplication.DoesNotExist:
            print("No applicants")
    except JobPosting.DoesNotExist:
        return redirect("RecruiterHome")
    
    return render(request,'recruiter/viewjob.html',{'job_details':job_details,'applicants':applicants})

def viewCandidateProfile(request,user_id):
    if request.user.is_authenticated:
        try:
            c_id=int(user_id)
            details = Candidate.objects.get(user_id=c_id)
            try:
                exp_details = Experience.objects.all().filter(candidate=details)
            except Experience.DoesNotExist:
                print("No experience")
            try:
                acc_details = Accomplishments.objects.all().filter(candidate=details)
            except Accomplishments.DoesNotExist:
                print("No accomplishments")
            try:
                project_details = Projects.objects.all().filter(candidate=details)
            except Projects.DoesNotExist:
                print("No Projects")
            try:
                skill_details = Skills.objects.all().filter(candidate=details)
            except Skills.DoesNotExist:
                print("No skills")
            try:
                language_details = Languages.objects.all().filter(candidate=details)
            except Languages.DoesNotExist:
                print("No languages")
            try:
                social_links = SocialLinks.objects.all().filter(candidate=details)
            except SocialLinks.DoesNotExist:
                print("no social links")
            context={
                'details':details,
                'exp_details':exp_details,
                'acc_details':acc_details,
                'project_details':project_details,
                'skill_details':skill_details,
                'language_details':language_details,
                'social_links':social_links,
            }
        except Candidate.DoesNotExist:
            print(" candidate doesn't exist")
    return render(request,'recruiter/viewCandidateProfile.html',context)

def shortlistCandidate(request,user_id,job_id):

    return redirect('viewJob')