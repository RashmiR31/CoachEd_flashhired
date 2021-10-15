from django.contrib import admin
from .models import User,Recruiter,JobPosting,Candidate
from django.contrib.auth.models import Group
# Register your models here.
admin.site.site_header = 'flashhired Administration' 
admin.site.unregister(Group)
#username = admin
#pw: CoachEdINAHAKPK.flashired21

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email']
    list_filter =['is_recruiter']

class RecruiterAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Recruiter,RecruiterAdmin)

class JobPostingAdmin(admin.ModelAdmin):
    list_display=['recruiter','job_title','salary']
    list_filter = ['job_type','date_posted']
admin.site.register(JobPosting,JobPostingAdmin)

admin.site.register(Candidate)
