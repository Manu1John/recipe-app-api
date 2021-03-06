from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,\
                                        PermissionsMixin
from django.conf import settings
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''creates and saves new user'''
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,password):
        '''creates and saves a new superuser'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    '''Custome user model that suppors using email insted of username'''
    email = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Tag(models.Model):
    '''tag to be used for a recipe'''
    name = models.CharField(max_length=100),
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    '''Ingredients to be used in a recipe'''
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name