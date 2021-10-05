from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User(AbstractUser):
    phone_number = PhoneNumberField()
    is_admin=models.BooleanField(default=False)
    is_candidate=models.BooleanField(default=False)
    is_recruiter=models.BooleanField(default=False)

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

class Recruiter(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=25,choices=GENDER_CHOICES)
    work_email = models.EmailField(max_length=254)
    dob = models.DateField()
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    experience = models.IntegerField()
    auth_doc = models.FileField(upload_to='uploads/rec/docs/')
    profile_pic = models.ImageField(upload_to='uploads/rec/pp/')

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
    upload_doc = models.FileField(upload_to='uploads/jp/docs/')

