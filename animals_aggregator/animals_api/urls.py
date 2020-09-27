from django.urls import path
from .views import AnimalDetail, AnimalList
urlpatterns = [
    path('<int:pk>/', AnimalDetail.as_view()),
    path('', AnimalList.as_view()),
]