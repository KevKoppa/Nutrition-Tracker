from django.contrib import admin  # here by default

# Register your models here.
from .models import Question  # import Question object
admin.site.register(Question)  # make Question objects accessible from admin site

