from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import BaseUserManager

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from uuid import uuid4
# from django.utils import timezone
# from datetime import timedelta

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email は必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user'

# class UserActivateTokenManager(models.Manager):

#     def activate_user_by_token(self, token):
#         pass
#         # user_activate_token = self.filter(
#         #     token = token,
#         #     expired_at_＿gte = timezone.now()
#         # ).first()
#         # if not user_activate_token:
#         #     raise ValueError('トークンが存在しません')
        
#         # user = user_activate_token.user
#         # user.sis_active = True
#         # user.savse()
#         # return user

#     def create_or_update_token(self, user):
#         token = str(uuid4())
#         expired_at = timezone.now() + timedelta(days=1)
#         user_token, created = self.update_or_create(
#             user=user,
#             defaults={'token': token, 'expired_at': expired_at,}
#         )
#         return user_token

# class UserActivateToken(models.Model):
#     token = models.UUIDField(db_index=True, unique=True)
#     expired_at = models.DateTimeField()
#     user = models.OneToOneField(
#         'User',
#         on_delete=models.CASCADE,
#         related_name='user_activate_token',   
#     )

    # objects: UserActivateTokenManager = UserActivateTokenManager()

    # class Meta:
    #     db_table = 'user_activate_token'

# @receiver(post_save, sender=User)
# def publish_token(sender, instance, created, **kwargs):
#     user_activate_token = UserActivateToken.objects.create_or_update_token(instance)
#     print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')