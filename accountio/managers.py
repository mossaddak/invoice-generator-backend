import logging

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

logger = logging.getLogger(__name__)


class CustomCustomerManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        password,
        is_staff,
        is_superuser,
        is_active=True,
        **kwargs
    ):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        username = username
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **kwargs):
        return self._create_user(username, email, password, False, False, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        return self._create_user(username, email, password, True, True, **kwargs)
