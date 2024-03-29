from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.




class MyAccountManager(BaseUserManager):
    def create_user(self,email,adhar,first_name,last_name,password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not adhar:
            raise ValueError("User must have an adhar")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            adhar=adhar,
            first_name=first_name,
            last_name=last_name,

        )
        user.set_password(password)
        user.save(using=self._db)
        return  user


    def create_superuser(self,email,adhar,first_name,last_name,password):
        user = self.create_user(
            email=self.normalize_email(email),
            adhar=adhar,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)

        return user









class Account(AbstractBaseUser):
    email           =models.EmailField(verbose_name="email",max_length=60,unique=True)
    adhar           =models.CharField(max_length=30,unique=True)
    date_joined     =models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login      =models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=True)
    is_staff        =models.BooleanField(default=False)
    is_superuser    =models.BooleanField(default=False)
    first_name      =models.CharField(max_length=30)
    last_name       =models.CharField(max_length=30)
    user_balance    =models.FloatField(default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['adhar','first_name','last_name']
    objects = MyAccountManager()
    def __str__(self):
        return (self.email+':'+self.adhar)

    def has_perm(self,perm,odj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
