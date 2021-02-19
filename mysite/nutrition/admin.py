from django.contrib import admin


# defines what attributes of Food model will define slug
class FoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


# Register your models here.
from .models import Food

admin.site.register(Food)
