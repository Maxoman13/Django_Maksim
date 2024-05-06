from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('thanks/', views.thanks_user, name='signup'),
]