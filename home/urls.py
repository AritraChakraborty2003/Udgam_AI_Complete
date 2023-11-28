from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('signUpConsumer',views.signupConsumer,name="signupconsumer"),
    path('loginConsumer',views.loginConsumer,name="login"),
    path('Payment',views.payment,name="Payment"),
    path('Loan',views.Loan,name="Payment"),
    path("logout",views.logout,name="dash1"),
    path("docVerify",views.docVerify,name="docVerify"),
    path("verification",views.verification,name="verification"),
    path("bankSide",views.bankSide,name="bankSide"),
    path("salesLogin",views.salesLogin,name="SalesLogin"),
    path("investLogin",views.investLogin,name="InvestLogin"),
    path("loanLogin",views.loanLogin,name="Loan"),
    path("logoutBank",views.logoutBank,name="LogoutBank"),
    path("investDashboard",views.investDashboard,name="LogoutBank"),
    path("marketingCampaign",views.marketingCampaign,name="marketCampaign"),


]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)