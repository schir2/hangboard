from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username: str, email: str, password: str, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
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


class Account(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(_('email address'), blank=True, unique=True,
        error_messages={'unique': _("A user with that username already exists."), }, )
    username = models.CharField(_('username'), max_length=150, unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator], error_messages={'unique': _("A user with that username already exists."), }, )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'), )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    birth_date = models.DateField(_('brith date'), default=timezone.datetime(year=1986, month=2, day=12))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        return True
