from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username: str, email: str, password: str, **extra_fields):
        """
        Create and save a user with the given handle, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, email: str = None, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username: str, email: str = None, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class Climber(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _('email address'),
        blank=True,
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

    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    preference = models.OneToOneField('Preference', on_delete=models.CASCADE)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        return self.is_active


class Profile(models.Model):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    birth_date = models.DateField(_('brith date'), default=timezone.datetime(year=1986, month=2, day=12))

    def __repr__(self):
        return f'Profile({self.first_name, self.last_name, self.birth_date})'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Preference(models.Model):
    MEASUREMENT_CHOICES = (
        ('METRIC', 'Metric'),
        ('IMPERIAL', 'Imperial'),
    )
    measurement = models.CharField(max_length=10, choices=MEASUREMENT_CHOICES, default='IMPERIAL')


class Stat(models.Model):
    logged = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    def get_measurement_system(self):
        pass

    class Meta:
        abstract = True


class Height(Stat):
    height = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.height}'


class Weight(Stat):
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.weight}'