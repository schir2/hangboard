from django.db.models import Manager, QuerySet
from django.utils.text import slugify
from django.utils import timezone


class SimpleModelManager(Manager):
    use_in_migrations = True

    def create_object(self, name: str, climber: str, slug: str = None, description: str = None, custom: bool = True,
                      **extra_fields):
        if not slug:
            slug = slugify(name, allow_unicode=True)
        if not description:
            description = name

        current_object = self.model(name=name, climber=climber, slug=slug, description=description, custom=custom,
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
            slug: str = None,
            description: str = None,
            custom: bool = True,
            #  logged=timezone.now().strftime('%Y %b %d %H %M %S'),
            logged=str(timezone.now()),
            **extra_fields,
    ):

        name = str(hangboard) if not name else name
        if not slug:
            slug = slugify(' '.join([name, str(logged)]), allow_unicode=True)
        if not description:
            description = name

        current_object = self.model(
            name=name,
            climber=climber,
            hangboard=hangboard,
            slug=slug,
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
            next_workout_set=None,
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
