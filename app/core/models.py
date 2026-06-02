from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin,
    BaseUserManager,
)


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
