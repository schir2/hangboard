from django.db.models import Manager
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

    def create_workout(
            self, name: str,
            climber: str,
            hangboard,
            slug: str = None,
            description: str = None,
            custom: bool = True,
            logged=timezone.now().strftime('%Y %b %d %H %M %S'),
            **extra_fields,
    ):

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
            **extra_fields,
        )
        current_object.save(using=self._db)
        return current_object
