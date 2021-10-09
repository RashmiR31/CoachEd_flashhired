from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from djongo import models
from django import forms
from django.forms import ModelForm

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

#################################################################################
##################### Candidate Side ############################################
#################################################################################

###################About############################
class Contact(models.Model):
    phone_number = PhoneNumberField()
    email_id = models.EmailField()
    alternate_email = models.EmailField()
    class Meta:
        abstract = True

class Address(models.Model):
    current = models.TextField()
    present = models.TextField()
    class Meta:
        abstract = True

class About(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=25,choices=GENDER_CHOICES)
    # contact = models.EmbeddedField(
    #     model_container=Contact,
    #     null=False
    # )
    # address = models.EmbeddedField(
    #     model_container=Address,
    #     null=False
    # )
    class Meta: 
        abstract = True

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('first_name','last_name','dob','gender')
##############################Education###############
class RecentEducation(models.Model):
    degree = models.CharField(max_length=100,choices = DEGREE_CHOICES)
    stream = models.CharField(choices = BRANCH_CHOICES)
    college_name = models.CharField(max_length=255)
    year_of_passing = models.DateField()
    percentage_cgpa = models.DecimalField()
    marks_card = models.FileField(upload_to='uploads/candidate/recent/markscards/',null=True)
    class Meta: 
        abstract = True

class PreUniversity(models.Model):
    combination = models.CharField(choices = COMBINATION_CHOICES)
    college_name = models.CharField(max_length=255)
    year_of_passing = models.DateField()
    percentage_cgpa = models.DecimalField()
    marks_card = models.FileField(upload_to='uploads/candidate/pu/markscards/',null=True)
    class Meta: 
        abstract = True

class SecondaryEducation(models.Model):
    school_name = models.CharField(max_length=255)
    year_of_passing = models.DateField()
    percentage_cgpa = models.DecimalField()
    marks_card = models.FileField(upload_to='uploads/candidate/secondary/markscards/',null=True)
    class Meta: 
        abstract = True

class Education(models.Model):
    recent = models.EmbeddedField(
        model_container=RecentEducation,
        null=False
    )
    pre_university = models.EmbeddedField(
        model_container=PreUniversity,
        null=False
    )
    secondary_education = models.EmbeddedField(
        model_container=SecondaryEducation,
        null=False
    )
    class Meta: 
        abstract = True

########################Work Experience#####################

############################################################

class Candidate(models.Model):
    about = models.EmbeddedField(
        model_container = About,
        model_form_class = AboutForm,
        null=False
    )
    # education = models.EmbeddedField(
    #     model_container = Education,
    #     null=False
    # )
    # work_experience = models.EmbeddedField(
    #     model_container = WorkExperience,
    #     null=False
    # )
    # accomplishments = models.EmbeddedField(
    #     model_container = Accomplishments,
    #     null=False
    # )
    # languages = models.EmbeddedField(
    #     model_container = Languages,
    #     null=False
    # )
    # projects = models.EmbeddedField(
    #     model_container = Projects,
    #     null=False
    # )
    # skills = models.EmbeddedField(
    #     model_container = Skills,
    #     null=False
    # )
    # social_handles = models.EmbeddedField(
    #     model_container = SocialHandles,
    #     null=False
    # )
    # resume = models.FileField(upload_to="upload/candidate/resumes/")
