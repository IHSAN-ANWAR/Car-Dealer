from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Static pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registration, name='register'),
    
    # API endpoints
    path('get_cars/', views.get_cars, name='get_cars'),
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('analyzereview/', views.sentiment_analyzer, name='analyze_review'),
]