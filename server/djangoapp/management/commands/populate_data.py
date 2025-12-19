from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel, CarDealer, DealerReview
from datetime import date

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample data...')
        
        # Create Car Makes
        toyota = CarMake.objects.get_or_create(
            name='Toyota',
            defaults={'description': 'Japanese automotive manufacturer known for reliability'}
        )[0]
        
        honda = CarMake.objects.get_or_create(
            name='Honda',
            defaults={'description': 'Japanese automotive manufacturer known for efficiency'}
        )[0]
        
        ford = CarMake.objects.get_or_create(
            name='Ford',
            defaults={'description': 'American automotive manufacturer'}
        )[0]
        
        # Create Car Models
        CarModel.objects.get_or_create(
            car_make=toyota, name='Camry', defaults={'type': 'SEDAN', 'year': 2023}
        )
        CarModel.objects.get_or_create(
            car_make=toyota, name='RAV4', defaults={'type': 'SUV', 'year': 2023}
        )
        CarModel.objects.get_or_create(
            car_make=honda, name='Civic', defaults={'type': 'SEDAN', 'year': 2023}
        )
        CarModel.objects.get_or_create(
            car_make=honda, name='CR-V', defaults={'type': 'SUV', 'year': 2023}
        )
        CarModel.objects.get_or_create(
            car_make=ford, name='F-150', defaults={'type': 'WAGON', 'year': 2023}
        )
        
        # Create Dealers
        dealers_data = [
            {
                'id': 1,
                'city': 'New York',
                'state': 'New York',
                'st': 'NY',
                'address': '123 Broadway Ave',
                'zip': '10001',
                'lat': 40.7128,
                'long': -74.0060,
                'short_name': 'NYC Motors',
                'full_name': 'New York City Motors'
            },
            {
                'id': 2,
                'city': 'Los Angeles',
                'state': 'California',
                'st': 'CA',
                'address': '456 Sunset Blvd',
                'zip': '90028',
                'lat': 34.0522,
                'long': -118.2437,
                'short_name': 'LA Auto',
                'full_name': 'Los Angeles Auto Center'
            },
            {
                'id': 3,
                'city': 'Houston',
                'state': 'Texas',
                'st': 'TX',
                'address': '789 Main St',
                'zip': '77002',
                'lat': 29.7604,
                'long': -95.3698,
                'short_name': 'Houston Cars',
                'full_name': 'Houston Car Dealership'
            },
            {
                'id': 4,
                'city': 'Miami',
                'state': 'Florida',
                'st': 'FL',
                'address': '321 Ocean Drive',
                'zip': '33139',
                'lat': 25.7617,
                'long': -80.1918,
                'short_name': 'Miami Motors',
                'full_name': 'Miami Beach Motors'
            },
            {
                'id': 5,
                'city': 'Wichita',
                'state': 'Kansas',
                'st': 'KS',
                'address': '555 Douglas Ave',
                'zip': '67202',
                'lat': 37.6872,
                'long': -97.3301,
                'short_name': 'Wichita Auto',
                'full_name': 'Wichita Auto Sales'
            }
        ]
        
        for dealer_data in dealers_data:
            CarDealer.objects.get_or_create(
                id=dealer_data['id'],
                defaults=dealer_data
            )
        
        # Create Sample Reviews
        reviews_data = [
            {
                'name': 'John Smith',
                'dealership': 1,
                'review': 'Fantastic service! The staff was very professional and helpful.',
                'purchase': True,
                'purchase_date': date(2023, 10, 15),
                'car_make': 'Toyota',
                'car_model': 'Camry',
                'car_year': 2023,
                'sentiment': 'positive'
            },
            {
                'name': 'Sarah Johnson',
                'dealership': 2,
                'review': 'Great experience buying my new Honda. Highly recommend!',
                'purchase': True,
                'purchase_date': date(2023, 11, 5),
                'car_make': 'Honda',
                'car_model': 'CR-V',
                'car_year': 2023,
                'sentiment': 'positive'
            },
            {
                'name': 'Mike Davis',
                'dealership': 3,
                'review': 'Poor customer service. Had to wait too long.',
                'purchase': False,
                'sentiment': 'negative'
            }
        ]
        
        for review_data in reviews_data:
            DealerReview.objects.get_or_create(
                name=review_data['name'],
                dealership=review_data['dealership'],
                defaults=review_data
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )