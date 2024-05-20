from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('thanks/', views.ThanksForRegister.as_view(), name='thanks_user'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path("password_change/", views.PasswordChange.as_view(), name='password_change'),
    path("passwor_change_done/", views.PasswordChangeDone.as_view(), name='password_change_done'),
]