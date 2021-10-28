from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import User,Candidate, Recruiter, JobPosting,WorkExperience,Accomplishments,Projects

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )

class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='IN')
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2','phone_number','is_candidate','is_recruiter')
    

class RecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = '__all__'
        exclude =('user',)

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields ='__all__'
        exclude =('recruiter',)

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        exclude=('user',)

class CandidateWorkExperienceForm(forms.ModelForm):
    class Meta:
        model=WorkExperience
        fields = '__all__'
        exclude=('candidate',)

class CandidateAccomplishmentsForm(forms.ModelForm):
    class Meta:
        model=Accomplishments
        fields = '__all__'
        exclude=('candidate',)

class CandidateProjectsForm(forms.ModelForm):
    class Meta:
        model= Projects
        fields = '__all__'
        exclude=('candidate',)