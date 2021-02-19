from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Food
import requests, re
from datetime import datetime

# API ID and Key
id = '61654da9'
key = '2bc123f14ee26003008a336ca46f5d5b'
# default date used for many pages
date = str(datetime.today().date())


# function for retrieving nutritional info for detail view
def Summary(food_list):
    calories = str(sum([food['calories'] for food in food_list])) + " calories"
    fat = str(round(sum([food['totalNutrients']['FAT']['quantity'] for food in food_list]), 3)) + " g"
    carbs = str(round(sum([food['totalNutrients']['CHOCDF']['quantity'] for food in food_list]), 3)) + " g"
    protein = str(round(sum([food['totalNutrients']['PROCNT']['quantity'] for food in food_list]), 3)) + " g"
    return {'calories': calories, 'fat': fat, 'carbs': carbs, 'protein': protein}


# list of foods eaten on a day on homepage
@login_required
def FoodListView(request, date_w):
    # if user wants to change the date they're viewing, this will handle it
    if request.method == 'POST':
        date_w = request.POST['date']

    # getting foods by meal from local database
    date_conv = datetime.strptime(str(date_w), '%Y-%m-%d').date()
    breakfast = Food.objects.filter(user=request.user, meal='BR', date=date_conv)
    lunch = Food.objects.filter(user=request.user, meal='LU', date=date_conv)
    dinner = Food.objects.filter(user=request.user, meal='DI', date=date_conv)
    snacks = Food.objects.filter(user=request.user, meal='SN', date=date_conv)

    # List of food's json objects from particular meal. JSON was pulled from Edamam API that gives nutritonal info.
    breakfast_data = [requests.get(
        "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code)).json()
                      for code in [re.sub(r'\s+', '%20', food.name) for food in breakfast]]
    lunch_data = [requests.get(
        "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code)).json()
                      for code in [re.sub(r'\s+', '%20', food.name) for food in lunch]]
    dinner_data = [requests.get(
        "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code)).json()
                      for code in [re.sub(r'\s+', '%20', food.name) for food in dinner]]
    snacks_data = [requests.get(
        "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code)).json()
                      for code in [re.sub(r'\s+', '%20', food.name) for food in snacks]]

    # food data for all foods
    food_data = [requests.get(
        "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code)).json()
                      for code in
                      [re.sub(r'\s+', '%20', food.name) for food in Food.objects.filter(user=request.user,
                                                                                        date=date_conv)]]

    # food data totals
    total_data = Summary(food_data)

    return render(request, 'nutrition/Food_list.html', {'breakfast': breakfast, "lunch": lunch, "dinner": dinner,
                                                        "snacks": snacks, 'breakfast_data': breakfast_data,
                                                        'lunch_data': lunch_data, 'dinner_data': dinner_data,
                                                        'snacks_data': snacks_data, "total_data": total_data,
                                                        "date": date_w})


# gives detailed nutrition info about singular Food
def detail(request, slug):
    food = get_object_or_404(Food, slug=slug)
    code = re.sub(r'\s+', '%20', food.name)
    response = requests.get(
        "https://api.edamam.com/api/nutrition-data?app_id={0}&app_key={1}&ingr=%20{2}".format(id, key, code))
    json_data = response.json()
    return render(request, 'nutrition/Food_detail.html', {'object': food, 'data': json_data, 'date': date})


# Form for adding new foods to food list
class CreateFoodView(CreateView):
    template_name = "nutrition/Food_form.html"
    model = Food
    fields = ['name', 'date', 'meal']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "date": date
        })
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


# Updates already created Food
class UpdateFoodView(UpdateView):
    model = Food
    context_object_name = 'food'
    fields = ['name', 'date', 'meal']
    template_name = "nutrition/Food_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "date": str(date)
        })
        return context


# Takes slug from delete url and identifies which Food to delete using given template
class DeleteFoodView(DeleteView):
    model = Food
    context_object_name = 'food'
    template_name = "nutrition/Food_delete.html"
    success_url = "/food-list/{}".format(date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "date": str(date)
        })
        return context


def ChangeDateView(request):
    return render(request, "nutrition/ChangeDate.html", {"date": date})
