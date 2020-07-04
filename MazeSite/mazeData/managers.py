from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, userName, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        
        if not userName or not password:
            raise ValueError(_('The Username or Password must be set'))

        user = self.model(userName=userName, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, userName, password):
        u = self.create_user(userName, password)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)

        return u
        