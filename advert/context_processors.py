from .models import Advert
import random


def fetch_advert(request):
    adverts = Advert.objects.filter(status=1)
    advert = random.choice(adverts)
    return {
        'advert': advert
    }
