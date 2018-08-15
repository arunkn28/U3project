from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import ugettext_lazy  as _

# Create your models here.
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    username        =   models.CharField(_('User Name'), max_length=50, unique=True)
    phone_number    =   models.CharField(_('Phone Number'), max_length=15, blank=True)
    email           =   models.EmailField(_('Email Id'), max_length=50, blank=True)
    adi             =   models.CharField(_('ADI'), max_length=20, blank=True)
    login_source    =   models.CharField(_('Login Source'), max_length=20, blank=True)
    
    objects         =   UserManager()
    USERNAME_FIELD  =   'username'
    REQUIRED_FIELDS =   ['email']

    class Meta:
        db_table = 's_t_userdetails'
    
    def __str__(self):
        return self.username

class MobileOTPTemp(models.Model):
    phone_number    =   models.CharField(_('Phone Number'), max_length=15, blank=True)
    otp             =   models.IntegerField(blank=True)

    class Meta:
        db_table = 's_t_temp'

    def __str__(self):
        return self.phone_number


class ResDetails(models.Model):
    res_name        = models.CharField(_('Phone Number'), max_length=50, blank=True)
    res_address     = models.CharField(_('Residentail Address'), max_length=100, blank=True)
    
    class Meta:
        db_table = 's_t_resDetails'
    
    def __str__(self):
        return self.res_name
    

class FeedBackLabel(models.Model):
    label          = models.CharField(_('Feedback Label'), max_length=10)
    
    class Meta:
        db_table = 's_t_feedback'
    
    def __str__(self):
        return self.label
    
     
class Rating(models.Model):
    user            = models.ForeignKey(User)
    label_code      = models.ForeignKey(FeedBackLabel)
    rating          = models.IntegerField()
    
    class Meta:
        db_table = 's_t_rating'     
    
class TableCode(models.Model):
    table_code = models.CharField(max_length=10, primary_key=True)
    res_code   = models.ForeignKey(ResDetails)
    
    class Meta:
        db_table = 's_t_tablecode' 
    
    def __str__(self):
        return self.table_code
    
        
class Category(models.Model):
    res_code        = models.ForeignKey(ResDetails)
    name            = models.CharField(max_length=50)
    sort            = models.IntegerField()
     
    class Meta:
        db_table = 's_t_cat'
         
    def __str__(self):
        return self.name
 
 
class Item(models.Model):
    res_code        = models.ForeignKey(ResDetails)
    name            = models.CharField(max_length=50)
    category        = models.ForeignKey(Category)
    sort            = models.IntegerField()
    description     = models.CharField(max_length=100)
    type            = models.CharField(max_length=10)
    price           = models.DecimalField(decimal_places=2,max_digits=7)
    availabilty     = models.BooleanField(default=False)
     
    class Meta:
        db_table = 's_t_item'
     
    def __str__(self):
        return self.name
 
 
class Order(models.Model):
    item            = models.ForeignKey(Item)
    item_quantity   = models.IntegerField()
    item_price      = models.DecimalField(decimal_places=2,max_digits=7)
    res_code        = models.ForeignKey(ResDetails)
    user            = models.ForeignKey(User)
    username        = models.CharField(max_length=50)
    delivered       = models.BooleanField(default=False)
    prepared        = models.BooleanField(default=False)
    order_time      = models.DateTimeField(blank=True)
    delivery_time   = models.DateTimeField(blank=True)
     
    class Meta:
        db_table = 's_t_placedorder'
     
    def __str__(self):
        self.order.id
 

class QRCode(models.Model):
    qr_code         = models.CharField(max_length=20, primary_key=True)
    res_code        = models.ForeignKey(ResDetails)
    table_code      = models.ForeignKey(TableCode)
    active          = models.BooleanField(default=False)
    order_code      = models.ForeignKey(Order) #Foreign key to Order table
    waiter          = models.BooleanField(default=False)
    freeze_bill     = models.BooleanField(default=False)
      
    class Meta:
        db_table = 's_t_qrcode'
      
    def __str__(self):
        return self.qr_code
    
     
class Table(models.Model):
    res_code        = models.ForeignKey(ResDetails)
    area_name       = models.CharField(max_length=25)
    num_of_tables   = models.IntegerField()
     
    class Meta:
        db_table = 's_t_table'
     
    def __str__(self):
        return self.area_name
 
     
class Variable(models.Model):
    var_name    = models.CharField(max_length=20, primary_key=True)
    var_value   = models.IntegerField()
     
    class Meta:
        db_table = 's_t_variable'
         
    def __str__(self):
        return self.var_name