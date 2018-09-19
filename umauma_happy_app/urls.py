from django.urls import path
from umauma_happy_app import views


app_name = 'umauma_happy_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('purchase/<int:race_id>', views.purchase, name='purchase'),
    path('purchase_do/', views.purchase_do, name='purchase_do'),
]
