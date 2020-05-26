from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from annoying.fields import AutoOneToOneField
from climbers.managers import UserManager


class Climber(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _('email address'),
        max_length=150,
        unique=True,
        error_messages={'unique': _("A user with that username already exists."), },
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists."), },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' \
               f'email={self.email},' \
               f'username={self.username},' \
               f'is_staff={self.is_staff},' \
               f'is_active={self.is_active},' \
               f'date_joined={self.date_joined})'

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        return self.is_active


class Profile(models.Model):
    climber = AutoOneToOneField(Climber, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    birth_date = models.DateField(_('birth date'), default=timezone.datetime(year=1986, month=2, day=12))
    gender = models.CharField(_('gender'), max_length=30, blank=True, null=True)

    def get_age(self):
        return timezone.now().year - self.birth_date.year
    get_age.short_description = 'age'

    def __repr__(self):
        return f'{self.__class__.__name__}(climber={self.climber}, ' \
               f'first_name={self.first_name}, ' \
               f'last_name={self.last_name}, ' \
               f'birth_date={self.birth_date})'

    def __str__(self):
        return f"{self.climber}'s Profile {self.first_name} {self.last_name}"


class Preference(models.Model):
    MEASUREMENT_CHOICES =(
        ('METRIC', 'Metric'),
        ('IMPERIAL', 'Imperial'),
    )

    climber = AutoOneToOneField(Climber, on_delete=models.CASCADE, primary_key=True)
    measurement_system = models.CharField(max_length=10, choices=MEASUREMENT_CHOICES, default='IMPERIAL')
    rest_between = models.PositiveIntegerField(default=10)
    rest_after = models.PositiveIntegerField(default=60)
    duration = models.PositiveIntegerField(default=10)

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'climber={self.climber}, ' \
               f'measurement_system={self.measurement_system},' \
               f'rest_between={self.rest_between},' \
               f'duration={self.duration})'

    def __str__(self):
        return f"{self.climber}'s Preferences"


class Measurement(models.Model):
    climber = AutoOneToOneField(Climber, on_delete=models.CASCADE, primary_key=True)

    def get_current_height(self):
        height = self.height_set.latest()
        return height if height else 0
    get_current_height.short_description = 'height'

    def get_current_weight(self):
        weight = self.weight_set.filter(measurement__climber=self.climber).all()
        return weight[-1] if weight else 0
    get_current_weight.short_description = 'weight'

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'climber={self.climber})'

    def __str__(self):
        return f"{self.climber}'s Measurements"


class BaseStat(models.Model):
    logged = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        get_latest_by = 'logged'


class Height(BaseStat):
    height = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.height}'


class Weight(BaseStat):
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.weight}'