import requests, json, datetime
from django.shortcuts import render
from .forms import CityForm
from django.utils import timezone
from geopy.geocoders import Nominatim


def get_weather(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            
            # GET GEOLOCATION FOR ENTERED CITY NAME
            geolocator = Nominatim(user_agent="GEO")         
            location = geolocator.geocode(city)
            latitude = location.latitude
            lat = round(latitude, 2)
            longitude = location.longitude
            long = round(longitude, 2)
            city_name = location.address.split(',')[0]
            
            # GET WEATHER DATA FROM API 
            api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true'
            response = requests.get(api_url)
            data = response.json()
            
            current_weather = data.get('current_weather')
            current_temp = current_weather.get('temperature')
            current_time = datetime.datetime.now().time().strftime('%H:%M')
            humidity = current_weather.get('relative_humidity')
            wind_speed = current_weather.get('windspeed')
            weather_code = current_weather.get('weathercode')
            weather_conditions = {
                0: 'Clear',
                1: 'Mainly clear',
                2: 'Partly cloudy',
                3: 'Overcast',
                45: 'Fog',
                48: 'Depositing rime fog',
                51: 'Light drizzle',
                53: 'Moderate drizzle',
                55: 'Dense drizzle',
                56: 'Light freezing drizzle',
                57: 'Dense freezing drizzle',
                61: 'Slight rain',
                63: 'Moderate rain',
                65: 'Heavy rain',
                66: 'Light freezing rain',
                67: 'Heavy freezing rain',
                71: 'Slight snow fall',
                73: 'Moderate snow fall',
                75: 'Heavy snow fall',
                77: 'Snow grains',
                80: 'Slight rain showers',
                81: 'Moderate rain showers',
                82: 'Violent rain showers',
                85: 'Slight snow showers',
                86: 'Heavy snow showers',
                95: 'Thunderstorm',
                96: 'Thunderstorm with slight hail',
                99: 'Thunderstorm with heavy hail'
            }
            weather_condition = weather_conditions.get(weather_code, 'Unknown')
            current_day = datetime.datetime.now().strftime('%A')
            
            
            # SAVE SESSION SEARCH
            if 'search_history' not in request.session:
                request.session['search_history'] = []

            city_names = [entry['city'] for entry in request.session['search_history']]
            if city_name not in city_names:
                request.session['search_history'].insert(0, {'city': city_name})
            request.session['search_history'] = request.session['search_history'][-10:]

            context = {
                'city_name':city_name,
                'data': data,
                'form': form,
                'humidity': humidity,
                'current_temp':current_temp,
                'current_time':current_time,
                'wind_speed': wind_speed,
                'weather_condition': weather_condition,
                'day_of_week': current_day,
                'search_history': request.session['search_history']
            }
            return render(request, 'index.html', context)

    else:
        form = CityForm()

    search_history = request.session.get('search_history', [])
    last_search = search_history[-1] if search_history else None

    return render(request, 'index.html', {'form': form, 'last_search': last_search})
