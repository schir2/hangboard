from django.test import TestCase

# Create your tests here.
from climbers.models import Climber

if __name__ == '__main__':

    test_climber = Climber.objects.get('schir2@gmail.com')