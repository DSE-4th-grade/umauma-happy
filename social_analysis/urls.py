from django.urls import path
from social_analysis import views


app_name = 'social_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:analysis_number>', views.index, name='index'),
]
