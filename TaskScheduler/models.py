from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),  # First is DB value, Second is Display Label
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    CATEGORY_CHOICES = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('School', 'School'),
        ('Urgent', 'Urgent'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Personal')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def sla_status(self):
        if self.is_completed:
            return 'DONE'
        now = timezone.now()
        if self.due_date < now:
            return 'LATE'
        elif self.due_date < now + timedelta(hours=24):
            return 'URGENT'
        elif self.due_date < now + timedelta(days=3):
            return 'WARNING'
        return 'SAFE'