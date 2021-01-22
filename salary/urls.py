from django.urls import path
from . import views

urlpatterns = [
    path('salary/create', views.salary_form, name='salary_insert'),
    path('salary/<int:id>/', views.salary_form, name='salary_update'),
    path('salary/delete/<int:id>/', views.salary_delete, name='salary_delete'),
    path('salaries/', views.salary_list, name='salary_list')
]