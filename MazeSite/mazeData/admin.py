from django.contrib import admin
from mazeData.models import Users, userData, highScores
# Register your models here.
admin.site.register(Users)
admin.site.register(userData)
admin.site.register(highScores)