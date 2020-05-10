from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.LoginPage),  # Login page
    url(r'^logout/', views.Logout),  # Logout
    url(r'^signup/', views.SignupPage),  # Signup Page
    url(r'^authentication/', views.LoginSubmit),  # Authentication
    url(r'^register/', views.SignUp),  # Authentication

    url(r'^home/', views.HomePage), #Home Page
    url(r'^profile/', views.Profile), #Profile Page
]