from django.urls import path
import scraping_module.views.scraping_view, scraping_module.views.data_convert_view

urlpatterns = [
    path('', scraping_module.views.scraping_view.index, name='index'),
]