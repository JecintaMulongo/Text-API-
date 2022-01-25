from django.contrib.auth.base_user import BaseUserManager



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True

    def create_user(self, email, password=None,**extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email")


        print('email', email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email= email)
        )

        user.set_password(password=password)  # change password to hash
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
