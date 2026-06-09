from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin,
    BaseUserManager,
)
from django.conf import settings
import os
import uuid


# All this will do is to modify the filename to an UUID.ext
def recipe_image_file_Path(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", new_filename)


# Since we are using AbstractBaseUser, it requires us to define the UserManager as below.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        # If you pass an email string to self.normalize_email(email), Django splits the string at the @ symbol, converts everything after it to lowercase, and stitches it back together.
        email = self.normalize_email(email)

        # self.model exposes the user's model.
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        # We can leave it just user.save(). But there may be a case where user info may be a part of a another DB so explicitly mentioning it.
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        superuser = self.create_user(email=email, password=password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

        return superuser


# I am inheriting the below fields from these both classes.

# AbstractBaseUser
# ├── password
# ├── last_login
# ├── set_password()
# └── check_password()

# PermissionsMixin
# ├── is_superuser
# ├── groups
# └── user_permissions()

# I am adding a few more based on my need.
# Your User
# ├── email
# ├── name
# ├── is_active
# └── is_staff


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # This makes us to treat email instead of username
    USERNAME_FIELD = "email"

    objects = UserManager()


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.URLField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField("Tag")
    image = models.ImageField(null=True, upload_to=recipe_image_file_Path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
