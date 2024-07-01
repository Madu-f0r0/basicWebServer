import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class HelloView(APIView):
    def get(self, request):
        visitor_name = request.query_params.get('visitor_name', 'Unspecified')
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))

        # Get client's location
        client_location_response = requests.get(f'https://ip-api.com/json/{client_ip}')
        client_location = client_location_response.json()
        city = client_location.get('city', 'Unknown')

        # Get weather for client's location
        weather_update = requests.get(f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={city}')
        weather_data = weather_update.json()
        temperature = weather_data.get('current', {}).get('temp_c', 'Unspecified')

        # Greeting response
        greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}'
        
        return Response({
            'client_ip': client_ip,
            'location': city,
            'greeting': greeting
        }, status=status.HTTP_200_OK)