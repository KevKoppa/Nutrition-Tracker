from django.urls import path
from . import views

app_name = 'polls'  # namespacing for organization
# path uses url name, view function that returns an HTTP response, kwargs, and a global name for your url
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create', views.QuestionCreate.as_view(), name='create-polls'),
    path('create2', views.ChoiceCreate.as_view(), name='create-choice'),
    path('updateQ/<int:pk>', views.QuestionUpdate.as_view(), name='update-question'),
    path('updateC', views.ChoiceUpdate.as_view(), name='update-choice')
]
