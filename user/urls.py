from django.urls import path
from . import views

urlpatterns = [
    path('create', views.user_form, name='user_insert'),
    path('<int:id>/', views.user_form, name='user_update'),
    path('delete/<int:id>/', views.user_delete, name='user_delete'),
    path('users/', views.user_list, name='user_list'),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.login_page, name="login"),
]