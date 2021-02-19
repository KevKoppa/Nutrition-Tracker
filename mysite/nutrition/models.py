from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
import re, requests
from django.http import HttpResponseRedirect


class Food(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(default=datetime.date.today)
    meal = models.CharField(max_length=2,
                            choices=[('BR', 'Breakfast'), ('LU', 'Lunch'), ('DI', 'Dinner'), ('SN', 'Snacks')],
                            default='BR')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    # for CreateView to create a url path to newly created Food objects
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("nutrition:food-detail", kwargs={"slug": self.slug})

    # saving Food objects to database
    def save(self, *args, **kwargs):
        self.name = self.name.lower()  # makes all food names lowercase for consistency
        self.slug = slugify(self.name)
        # FIXME - self.slug should be like below
        # self.slug = str(self.meal) + "-" + slugify(self.name) + "-" + str(self.date)
        super(Food, self).save(*args, **kwargs)

    # gets nutrition data about food from API
    def getData(self, name):
        id = 'e302d382'
        key = '1de405bcf0d2f70a5ca5b0a4724261ae'
        code = re.sub(r'\s+', '%20', self.name)
        response = requests.get(
            "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code))
        json_data = response.json()


# Model for changing date of food object you want to see
class Date(models.Model):
    date = models.DateField(default=datetime.date.today)
