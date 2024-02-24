from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path ('login/', views.login_view, name='login'),
    path ('logout/', views.logout_view, name='logout_view'),
    path ('sign-up/', views.signup_view, name='sign_up'),
    
    path ('dashboard/', views.dashboard, name = 'dashboard'),
    path ('home/', views.landingpage, name = 'home'),
    path ('about/', views.aboutpage, name = 'about_us'),
    path ('experience/', views.experience, name = 'experience'),
    path ('experience/adventure/', views.adventure, name = 'adventure'),
    path ('experience/culinary/', views.culinary, name = 'culinary'),
    path ('experience/cultural/', views.cultural, name = 'cultural'),
    path ('experience/luxury/', views.luxury, name = 'luxury'),
    path ('time-and-date/', views.TandD, name = 'time_and_date'),
    path ('schedule-trip/', views.schedule_trip, name = 'schedule_trip'),

    path ('dashboard/review', views.review, name = 'review'),
    path('callback/', views.callback_view, name='callback'),


]