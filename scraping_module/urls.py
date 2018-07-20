from django.urls import path


# from . import views.sc
import scraping_module.views.scraping_view

urlpatterns = [
    path('', scraping_module.views.scraping_view.index, name='index'),
]