from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("user_type", 1)
        extra_fields.setdefault("gender", 'M')
        extra_fields.setdefault("is_superuser", True)
        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE = ((1, "Manager"), (2, "Staff"), (3, "Customer"))
    GENDER = [("M", "Male"), ("F", "Female")]
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.IntegerField(choices=USER_TYPE)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(null=False)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name


# Customers
class Customer(models.Model):
    ACCOUNT_TYPE = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE)
    account_number = models.CharField(max_length=15)
    pin = models.CharField(max_length=4)
    date_of_birth = models.DateField()
    balance = models.FloatField()
    phone = models.CharField(max_length=11)
