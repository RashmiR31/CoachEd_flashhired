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

    path('candidate/',views.CandidateHome,name='CandidateHome'),
    path('candidate/createprofile',views.candidateCreateProfile,name='candidateCreateProfile'),
    path('candidate/profile',views.candidateProfile,name='candidateProfile'),
    path('candidate/profile/edit',views.candidateEditProfile,name='candidateEditProfile'),
    # work experience
    path('candidate/experience',views.candidateExperience,name='candidateExperience'),
    path('candidate/editexperience/<int:exp_id>',views.editExperience,name="editExperience"),
    path('candidate/deleteexperience/<int:exp_id>',views.deleteExperience,name="deleteExperience"),
    # accomplishments
    path('candidate/accomplishments',views.candidateAccomplishments,name='candidateAccomplishments'),
    path('candidate/editaccomplishments/<int:acc_id>',views.editAccomplishments,name="editAccomplishments"),
    path('candidate/deleteaccomplishments/<int:acc_id>',views.deleteAccomplishments,name="deleteAccomplishments"),
    # projects
    path('candidate/projects',views.candidateProjects,name='candidateProjects'),
    path('candidate/editprojects/<int:project_id>',views.editProjects,name="editProjects"),
    path('candidate/deleteprojects/<int:project_id>',views.deleteProjects,name="deleteProjects"),
    # skills
    path('candidate/skills',views.candidateSkills,name='candidateSkills'),
    path('candidate/editskills/<int:skill_id>',views.editSkills,name="editSkills"),
    path('candidate/deleteskills/<int:skill_id>',views.deleteSkills,name="deleteSkills"),
    # languages 
    path('candidate/languages',views.candidateLanguages,name='candidateLanguages'),
    path('candidate/editlanguages/<int:lan_id>',views.editLanguages,name="editLanguages"),
    path('candidate/deletelanguages/<int:lan_id>',views.deleteLanguages,name="deleteLanguages"),
    # socialhandles
    # path('candidate/socialhandles',views.candidateSocialHandles,name='candidateSocialHandles'),
    # path('candidate/editsocialhandles/<int:sh_id>',views.editSocialHandles,name="editSocialHandles"),
    ######## Recruiter Section #####################
    path('recruiter/',views.RecruiterHome,name='RecruiterHome'),
    path('recruiter/createprofile',views.recruiterCreateProfile,name="recruiterCreateProfile"),
    path('recruiter/profile',views.recruiterProfile,name='recruiterProfile'),
    path('recruiter/profile/edit',views.recruiterEditProfile,name='recruiterEditProfile'),
    path('recruiter/addjob',views.addJob,name="addJob"),
    path('recruiter/editjob/<int:job_id>',views.editJob,name="editJob"),
    path('recruiter/deletejob/<int:job_id>',views.deleteJob,name="deleteJob"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
