from django.contrib import admin
from .models import User
# Register your models here.
admin.site.site_header = 'flashHired Administration' 
#username = admin
#pw: CoachEdINAHAKPK.flashired21

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email']