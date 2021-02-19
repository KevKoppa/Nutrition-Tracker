from django.urls import path
from . import views

app_name = "nutrition"

urlpatterns = [
    path('food-list/<str:date_w>', views.FoodListView, name='food-list'),
    path('food-detail/<slug:slug>', views.detail, name='food-detail'),
    path('food-create', views.CreateFoodView.as_view(), name='food-create'),
    path('food-update/<slug:slug>', views.UpdateFoodView.as_view(), name='food-update'),
    path('food-delete/<slug:slug>', views.DeleteFoodView.as_view(), name='food-delete'),
    path('date-change', views.ChangeDateView, name="change-date")
]