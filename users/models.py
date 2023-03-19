from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
from .utils import rename_imagefile_to_uuid
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    
    class Types(models.TextChoices):
        CONSUMER = "CONSUMER", "소비자"
        ORGANIZATION = "ORGANIZATION", "환경단체"
    
    type = models.CharField(_('Type'), max_length=15, choices=Types.choices)
    email = models.EmailField("이메일", max_length=100, unique=True,)
    nickname = models.CharField("닉네임", max_length=10, unique=True,)
    profile_image = models.ImageField(default='/default_profile/default.PNG', upload_to=rename_imagefile_to_uuid, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# 프록시 모델 생성

class ConsumerManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CONSUMER)


class Consumer(User):
    objects = ConsumerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    

class OrganizationManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ORGANIZATION)


class Organization(User):
    objects = OrganizationManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


