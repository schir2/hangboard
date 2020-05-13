from django.db.models.signals import pre_delete
from main.models import WorkoutSet


def delete_pre(sender, instance, **kwargs):
    previous_workout_set = instance.previous
    next_workout_set = WorkoutSet.objects.filter(previous=instance.pk)
    if next_workout_set:
        next_workout_set[0].previous = previous_workout_set
        next_workout_set[0].save()


pre_delete.connect(delete_pre, WorkoutSet)
