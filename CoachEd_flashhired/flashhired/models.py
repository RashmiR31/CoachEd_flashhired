from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from djongo import models
from django import forms
from django.forms import ModelForm
from CoachEd_flashhired import settings
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
    date_posted = models.DateField()
    upload_doc = models.FileField(upload_to='recruiter/jobs/docs/')
    

#################################################################################
##################### Candidate Side ############################################
#################################################################################


class Candidate(models.Model):
    name= models.CharField(max_length=255)