from django.contrib import admin
from .models import User,Recruiter,JobPosting,Candidate
# Register your models here.
admin.site.site_header = 'flashHired Administration' 
#username = admin
#pw: CoachEdINAHAKPK.flashired21

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email']

class RecruiterAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Recruiter,RecruiterAdmin)

class JobPostingAdmin(admin.ModelAdmin):
    list_display=['recruiter','job_title']
admin.site.register(JobPosting,JobPostingAdmin)

admin.site.register(Candidate)
