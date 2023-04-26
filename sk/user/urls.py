from django.urls import path
from . import views 


app_name= "user"

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register , name="register"),
    path('login_user/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name="logout"),
    path('profile_list/', views.profile_list, name="profile-list"),
    path('profile/<int:id>/', views.profile , name="profile"),
    path('search_profile/', views.search_profile, name="search-profile")
]