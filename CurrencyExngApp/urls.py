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
    
    url(r'^create-wallet/', views.CreateWallet), #Create Wallet
    url(r'^add-money-to-wallet/', views.AddMoney), #Add Money to Wallet API
    url(r'^send-money-to-user/', views.SendMoney), #Send Money to User API
    url(r'^convert-currency/', views.ConvertCurrency), #Convert Currency API

    url(r'^save-profile/', views.SaveProfile), #Save Profile Data
]