from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_review, name='add_review'),
    path('search/', views.search_view, name='search'),
    path('login/', views.login_view, name='login'),
    path('delete/<int:id>/', views.delete_review, name='delete_review'),
]