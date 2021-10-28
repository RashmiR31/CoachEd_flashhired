"""CoachEd_flashhired URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from flashhired import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.pilot,name='pilot'),
    path('rechome/',views.rechome,name='rechome'),
    ######## authentication section ###############
    path('login/',views.login_view,name='login_view'),
    path('signupchoice/',views.SignupChoice,name='signupchoice'),
    path('recruitersignup/',views.recruiterSignup,name='recruitersignup'),
    path('candidatesignup/',views.candidateSignup,name='candidatesignup'),
    path('logout/',views.logout_view,name='logout_view'),
    path('password_reset/',views.password_reset_request,name="password_reset"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),name="password_reset_complete"),
    ######## Candidate Section #####################
    path('candidatehome/',views.CandidateHome,name='CandidateHome'),
    ######## Recruiter Section #####################
    path('recruiter/',views.RecruiterHome,name='RecruiterHome'),
    path('recruiter/createprofile',views.recruiterCreateProfile,name="recruiterCreateProfile"),
    path('recruiter/profile',views.recruiterProfile,name='recruiterProfile'),
    path('recruiter/profile/edit',views.recruiterEditProfile,name='recruiterEditProfile'),
    path('recruiter/addjob',views.addJob,name="addJob"),
    path('recruiter/editjob/<int:job_id>',views.editJob,name="editJob"),
    path('recruiter/deletejob/<int:job_id>',views.deleteJob,name="deleteJob"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
