from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']
    list_filter = ['car_make', 'type', 'year']
    search_fields = ['name', 'car_make__name']


@admin.register(CarDealer)
class CarDealerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'city', 'state', 'st']
    list_filter = ['state', 'st']
    search_fields = ['full_name', 'city', 'state']


@admin.register(DealerReview)
class DealerReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'dealership', 'sentiment', 'purchase']
    list_filter = ['sentiment', 'purchase']
    search_fields = ['name', 'review']