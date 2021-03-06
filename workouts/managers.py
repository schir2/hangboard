from django.db.models import Manager, QuerySet
from django.utils.text import slugify
from django.utils import timezone


class SimpleModelManager(Manager):
    use_in_migrations = True

    def create_object(self, name: str, climber: str, description: str = None, custom: bool = True,
                      **extra_fields):

        if not description:
            description = name

        current_object = self.model(name=name, climber=climber, description=description, custom=custom,
                                    **extra_fields)
        current_object.save(using=self._db)
        return current_object


class WorkoutManager(Manager):
    use_in_migrations = True

    def add_workout(
            self,
            climber: str,
            hangboard,
            name: str = None,
            description: str = None,
            custom: bool = True,
            logged=str(timezone.now()),
            **extra_fields,
    ):

        name = str(hangboard) if not name else name
        if not description:
            description = name

        current_object = self.model(
            name=name,
            climber=climber,
            hangboard=hangboard,
            description=description,
            custom=custom,
            logged=logged,
            **extra_fields,
        )
        current_object.save(using=self._db)
        return current_object


class WorkoutSetQuerySet(QuerySet):

    def get_next(self, previous):
        self.get(previous= previous)


class WorkoutSetManager(Manager):
    use_in_migrations = True

    def add_workout_set(
            self,
            climber: str,
            exercise: int,
            workout: int,
            previous=None,
            left_hold: int = None,
            left_fingers: int = 4,
            right_hold: int = None,
            right_fingers: int = 4,
            duration: int = 0,
            weight: int = 0,
            reps: int = 1,
            completed: int = True,
            logged=str(timezone.now()),
            **extra_fields,
    ):

        """ Find the next workout set before current_workout_set is created to avoid current_workout_set pointing to
        # itself when previous is none"""
        next_workout_set_queryset = self.filter(previous_id=previous.pk) if previous else self.filter(workout=workout, previous=None)
        next_workout_set = next_workout_set_queryset.all()[0] if next_workout_set_queryset else None

        current_workout_set = self.model(
            climber=climber,
            exercise=exercise,
            workout=workout,
            previous=previous,
            left_hold=left_hold,
            left_fingers=left_fingers,
            right_hold=right_hold,
            right_fingers=right_fingers,
            duration=duration,
            weight=weight,
            reps=reps,
            completed=completed,
            logged=logged,
            **extra_fields,
        )
        current_workout_set.save(using=self._db)

        if next_workout_set:
            next_workout_set.previous = current_workout_set
            next_workout_set.save(using=self.db)

        return current_workout_set
