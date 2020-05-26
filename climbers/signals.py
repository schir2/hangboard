from django.db.models.signals import post_save
from climbers.models import Climber


def post_save_climber(sender, instance, **kwargs):
    instance.profile
    instance.preference
    instance.measurement
    

post_save.connect(post_save_climber, Climber)
