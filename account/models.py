from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


from django.contrib.auth.hashers import PBKDF2PasswordHasher as has
# Create your models here.




class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, is_trainer, password, gender, birth_date=None, height=None, weight=None):
        if not email:
            raise ValueError('Must have email')

        if not first_name:
            raise ValueError('Must have first name')
        
        if not last_name:
            raise ValueError('Must have last name')


        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            height=height,
            weight=weight,
            is_trainer=is_trainer,
            gender = gender
        )

       

        user.set_password(password)
        user.save(using=self._db)

      
        return user

        


    def create_superuser(self, email, password, first_name, last_name):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_trainer=False,
            gender='M'
        )
        


        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


        return user



class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default=None) 


    height = models.IntegerField(validators = [MinValueValidator(120), 
        MaxValueValidator(230)], help_text='Enter your height in centimetres.', null=True, blank=True)
    weight = models.FloatField(validators = [MinValueValidator(30), 
        MaxValueValidator(350)], help_text='Enter your weight in kilograms.', null=True, blank=True) 
    birth_date = models.DateField(null=True, blank=True)
    
    about = models.TextField(max_length=1000, help_text='Say something about you.', null=1, blank=1)
    quote = models.CharField(max_length=30, help_text='', null=1, blank=1)

    trainer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        
    )
    gender = models.CharField(max_length=1, choices=GENDER)
    is_trainer = models.BooleanField(default=False)
    
 
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        ordering = ['id']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self,per,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    
    def get_request_number(self):
        return self.trainer_request.count()