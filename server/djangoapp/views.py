from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from .models import CarMake, CarModel, CarDealer, DealerReview


def index(request):
    """Home page view"""
    return render(request, 'index.html')


def about(request):
    """About page view"""
    return render(request, 'About.html')


def contact(request):
    """Contact page view"""
    return render(request, 'Contact.html')


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """User login endpoint"""
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
        else:
            return JsonResponse({
                "userName": username,
                "error": "Invalid credentials"
            }, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def logout_user(request):
    """User logout endpoint"""
    try:
        logout(request)
        return JsonResponse({"userName": "", "status": "Logged out"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def registration(request):
    """User registration endpoint"""
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "userName": username,
                "error": "Already Registered"
            }, status=400)
        
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        login(request, user)
        return JsonResponse({
            "userName": username,
            "status": "Authenticated"
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(['GET'])
def get_cars(request):
    """Get all car makes and models"""
    try:
        car_models = []
        for make in CarMake.objects.all():
            for model in CarModel.objects.filter(car_make=make):
                car_models.append({
                    "CarMake": make.name,
                    "CarModel": model.name,
                    "CarYear": model.year,
                    "CarType": model.type
                })
        return JsonResponse({"CarModels": car_models})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
def get_dealerships(request, state=None):
    """Get dealerships, optionally filtered by state"""
    try:
        if state:
            dealers = CarDealer.objects.filter(st=state.upper())
        else:
            dealers = CarDealer.objects.all()
        
        dealer_list = []
        for dealer in dealers:
            dealer_list.append({
                "id": dealer.id,
                "city": dealer.city,
                "state": dealer.state,
                "st": dealer.st,
                "address": dealer.address,
                "zip": dealer.zip,
                "lat": dealer.lat,
                "long": dealer.long,
                "short_name": dealer.short_name,
                "full_name": dealer.full_name
            })
        
        return JsonResponse({"status": 200, "dealers": dealer_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
def get_dealer_details(request, dealer_id):
    """Get dealer details by ID"""
    try:
        dealer = CarDealer.objects.get(id=dealer_id)
        dealer_data = {
            "id": dealer.id,
            "city": dealer.city,
            "state": dealer.state,
            "st": dealer.st,
            "address": dealer.address,
            "zip": dealer.zip,
            "lat": dealer.lat,
            "long": dealer.long,
            "short_name": dealer.short_name,
            "full_name": dealer.full_name
        }
        return JsonResponse({"status": 200, "dealer": dealer_data})
    except CarDealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
def get_dealer_reviews(request, dealer_id):
    """Get reviews for a specific dealer"""
    try:
        reviews = DealerReview.objects.filter(dealership=dealer_id)
        review_list = []
        for review in reviews:
            review_list.append({
                "id": review.id,
                "name": review.name,
                "dealership": review.dealership,
                "review": review.review,
                "purchase": review.purchase,
                "purchase_date": review.purchase_date.isoformat() if review.purchase_date else None,
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year,
                "sentiment": review.sentiment
            })
        
        return JsonResponse({"status": 200, "reviews": review_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    """Add a new review"""
    try:
        data = json.loads(request.body)
        
        # Get sentiment analysis
        sentiment = analyze_review_sentiment(data.get('review', ''))
        
        review = DealerReview.objects.create(
            name=data.get('name'),
            dealership=data.get('dealership'),
            review=data.get('review'),
            purchase=data.get('purchase', False),
            purchase_date=data.get('purchase_date'),
            car_make=data.get('car_make'),
            car_model=data.get('car_model'),
            car_year=data.get('car_year'),
            sentiment=sentiment
        )
        
        return JsonResponse({
            "status": 200,
            "message": "Review added successfully",
            "review_id": review.id
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def analyze_review_sentiment(review_text):
    """Analyze sentiment of review text using Flask microservice"""
    try:
        response = requests.post(
            'http://localhost:5000/analyzereview',
            json={'review': review_text},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('sentiment', 'neutral')
        else:
            return 'neutral'
    except:
        return 'neutral'


@api_view(['POST'])
def sentiment_analyzer(request):
    """Direct sentiment analysis endpoint"""
    try:
        data = request.data
        review_text = data.get('review', '')
        sentiment = analyze_review_sentiment(review_text)
        return Response({
            "sentiment": sentiment,
            "review": review_text
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)