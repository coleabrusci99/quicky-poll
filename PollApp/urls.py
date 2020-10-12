from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<url>/', views.voting_page, name='voting_page'),
    path('<url>/results/', views.results_page, name='results_page'),
]