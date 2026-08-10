from django.urls import path
from . import views

app_name = 'analitik'

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard'),
    path('admin/', views.DashboardAdminView.as_view(), name='dashboard_admin'),
    path('saya/', views.DashboardUserView.as_view(), name='dashboard_user'),
]
