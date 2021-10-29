from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from djongo import models
from django import forms
from django.forms import ModelForm
from CoachEd_flashhired import settings
from django.utils import timezone
import uuid
# Create your models here.

class User(AbstractUser):
    phone_number = PhoneNumberField()
    is_admin=models.BooleanField(default=False)
    is_candidate=models.BooleanField(default=False)
    is_recruiter=models.BooleanField(default=False)


##################### CHOICES ############################################

GENDER_CHOICES = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other'),
)

JOB_TYPE=(
    ('fulltime','Full Time'),
    ('internship','Internship'),
    ('contract','Contract'),
)

DEGREE_CHOICES = (
    ('b.e','B.E'),
    ('b.tech','B.Tech'),
    ('m.tech','M.Tech'),
    ('msc','MSc'),
)

BRANCH_CHOICES = (
    ('computerscience','Computer Science'),
    ('informationscience','Information Science'),
    ('electronicsandcommunication','Electronics and Communication'),
    ('mechanical','Mechanical'),
    ('civil','Civil'),
)

COMBINATION_CHOICES= (
    ('pcmb','PCMB'),
    ('pcmcs','PCMCs'),
    ('pcme','PCME'),
)

#################################################################################
##################### Recruiter Side ############################################
#################################################################################

class Recruiter(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=25,choices=GENDER_CHOICES,blank=True)
    work_email = models.EmailField(max_length=254,blank=True)
    phone_number =PhoneNumberField()
    dob = models.DateField()
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    experience = models.IntegerField()
    auth_doc = models.FileField(upload_to='recruiter/auth_doc/')
    profile_pic = models.ImageField(upload_to='recruiter/profile_pic/')
    def __str__(self):
        return self.name

class JobPosting(models.Model):
    recruiter = models.ForeignKey("Recruiter",on_delete=models.CASCADE)
    job_type = models.CharField(max_length=25,choices=JOB_TYPE)
    job_title = models.CharField(max_length=255)
    functional_area = models.CharField(max_length=255)
    jd = models.TextField()
    required_skills = models.TextField()
    required_experience = models.IntegerField()
    required_education = models.TextField()
    salary = models.IntegerField()
    is_negotiable = models.BooleanField(default=False)
    job_location = models.TextField()
    date_posted = models.DateField(default=timezone.now)
    upload_doc = models.FileField(upload_to='recruiter/jobs/docs/')
    

#################################################################################
##################### Candidate Side ############################################
#################################################################################


class Candidate(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        primary_key=True,
    )
    #About
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=25,choices=GENDER_CHOICES,blank=True)
    phone_number = PhoneNumberField()
    email_id = models.EmailField(max_length=254)
    alternate_email_id = models.EmailField(max_length=254)
    current_address = models.TextField()
    permanent_address = models.TextField()
    profile_pic = models.ImageField(upload_to='candidate/profile_pic/',null=True)
    #Education 
    #recent
    recent_degree = models.CharField(max_length=10)
    recent_stream = models.CharField(max_length=255)
    recent_college_name = models.CharField(max_length=255)
    recent_yop = models.DateField(default=timezone.now)
    recent_cgpa_equivalent = models.DecimalField(max_digits=4,decimal_places=2)
    recent_marks_card = models.FileField(upload_to='candidate/recent/marks_card/')
    #PU
    pu_combination = models.CharField(max_length=100)
    pu_college_name = models.CharField(max_length=100)
    pu_yop = models.DateField(default=timezone.now)
    pu_percentage = models.DecimalField(max_digits=4,decimal_places=2)
    pu_marks_card = models.FileField(upload_to='candidate/pu/marks_card/')
    #10th
    tenth_school_name = models.CharField(max_length=100)
    tenth_yop = models.DateField(default=timezone.now)
    tenth_percentage = models.DecimalField(max_digits=4,decimal_places=2)
    tenth_marks_card = models.FileField(upload_to='candidate/tenth/marks_card/')
    #Work Experience


class Accomplishments(models.Model):
    candidate = models.ForeignKey("Candidate",on_delete = models.CASCADE)
    certificate_name = models.CharField(max_length=255,null=True)
    certificate_issued_by = models.CharField(max_length=100,null=True)
    certificate_issue_date= models.DateField(default=timezone.now,null=True)
    certificate_link = models.CharField(max_length=5000,null=True)
    certificate_doc = models.FileField(upload_to='candidate/certificates/')
    award_name = models.CharField(max_length=255)
    award_issued_by = models.CharField(max_length=255)

class Projects(models.Model):
    candidate = models.ForeignKey("Candidate",on_delete = models.CASCADE)
    project_name = models.CharField(max_length=255)
    technologies_used = models.CharField(max_length=255)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=timezone.now)
    description = models.TextField()
    supporting_media_or_link = models.CharField(max_length=5000)

class Experience(models.Model):
    candidate = models.ForeignKey("Candidate",on_delete = models.CASCADE)
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    supporting_doc = models.FileField(upload_to='candidate/experience/')

class Skills(models.Model):
    candidate = models.ForeignKey("Candidate",on_delete = models.CASCADE)
    skill_name = models.CharField(max_length=50)
    rating = models.IntegerField()
    supporting_doc = models.FileField(upload_to='candidate/skills')

class Languages(models.Model):
    candidate = models.ForeignKey("Candidate",on_delete = models.CASCADE)
    language = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=50)

class SocialLinks(models.Model):
    candidate = models.ForeignKey("Candidate",on_delete=models.CASCADE)
    facebook = models.URLField(max_length=500,blank=True)
    instagram =models.URLField(max_length=500,blank=True)
    linkedin =models.URLField(max_length=500,blank=True)
    github =models.URLField(max_length=500,blank=True)
    personal_website =models.URLField(max_length=500,blank=True)
    codechef =models.URLField(max_length=500,blank=True)
    hackerrank =models.URLField(max_length=500,blank=True)
    kaggle=models.URLField(max_length=500,blank=True)
    twitter=models.URLField(max_length=500,blank=True)
    dribble=models.URLField(max_length=500,blank=True)
    other=models.URLField(max_length=500,blank=True)