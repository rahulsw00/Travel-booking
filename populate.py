import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()


from faker import Faker
import random
from app.models import travelOptions, city
from datetime import datetime
from dateutil.relativedelta import relativedelta



faker = Faker()

cities = ["Delhi", "Mumbai", "Kolkata", "Bangalore", "Chennai", "Hydrabad", "Ahmedabad", "Surat", "Pune", "Jaipur"]

for c in cities:
    city.objects.get_or_create(name=c)

allCities = list(city.objects.all())
for _ in range(100):
    src, dest = random.sample(allCities, 2)
    travelOptions.objects.create(
        source = src,
        destination = dest,
        travelType = random.choice(["Flight", "Bus", "Train"]),
        price = random.randint(5, 200) * 100,
        availableSeats = random.randint(0, 50),
        dateTime = faker.date_time_between_dates(datetime_start=datetime.now(), datetime_end=datetime.now() + relativedelta(months=1))
    )