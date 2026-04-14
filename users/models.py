from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field cannot be empty')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=true')
        elif not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=true')
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'
    
    
    username = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def clean(self):
        fields = ['country', 'city', 'address', 'postal_code']
        for field in fields:
            value = getattr(self, field)
            if value:
                setattr(self, field, strip_tags(value))
    