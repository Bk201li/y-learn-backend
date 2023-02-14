from django.db import models
from uuid import uuid4
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email address",
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    STUDENT = "student"
    TEACHER = "teacher"

    TYPE_USER = [
        (STUDENT, "student"),
        (TEACHER, "teacher")
    ]

    status = models.CharField(
        max_length=7,
        choices=TYPE_USER
    )

    def __str__(self):
        return self.email

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

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True, max_length=255)

    def __str__(self):
        return self.label

class Exercice(models.Model):
    id: models.UUIDField(primary_key=True, default=uuid4, editable=False)
    label: models.TextField(max_length=150)
    answer: models.TextField(max_length=150)
    doneBy: models.ForeignKey(MyUser, related_name='student', on_delete=models.CASCADE)
    createdBy: models.ForeignKey(MyUser, related_name='teacher', on_delete=models.CASCADE)
    categoryId: models.ForeignKey(Category, related_name='type_exercice', on_delete=models.CASCADE)


