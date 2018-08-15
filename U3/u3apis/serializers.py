import random
from django.contrib.auth import authenticate, login

from rest_framework.serializers import (
    CharField,
    IntegerField,
    Serializer,
    ValidationError,
    ModelSerializer
    )

from .models import *


class ProfileSerializer(Serializer):
    task_flag        = IntegerField()
    password         = CharField(style={'input_type': 'password'}, trim_whitespace=False, required=False)
    email            = CharField()
    phone_number     = CharField(required=False)
    adi              = CharField()
    username         = CharField()
    otp              = IntegerField(required=False)
    login_source     = CharField()
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password', 'auth_token', 'phone_number','adi','task_flag',)
#         read_only_fields = ('auth_token',)
#         extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        task_flag       = data.get('task_flag')
        email           = data.get('email')
        password        = data.get('password')
        phone_number    = data.get('phone_number')
        adi             = data.get('adi')
        username        = data.get('username')
        otp             = data.get('otp')
        login_source    = data.get('login_source')
        if task_flag ==1:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError({'code':20601})
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise ValidationError({'ERR':'Cannot Authenticate'})
            user.username = username
            user.login_source = login_source
            user.adi = adi
            user.save()
            data['user'] = user
            data['code'] = 20600
        elif task_flag == 2:
            try:
                otp_new = random.randint(1000,9999)
                mobile_otp_obj = MobileOTPTemp.objects.get(phone_number=phone_number)
                if int(mobile_otp_obj.otp)!=otp:
                    raise ValueError
                else:
                    try:
                        user = User.objects.get(phone_number=phone_number)
                        user.email = email
                        user.username = username
                        user.login_source = login_source
                        user.adi = adi
                        data['code']= 20602
                    except:
                        user = User.objects.create_user(email=email,
                                                        phone_number=phone_number,
                                                        adi=adi,
                                                        username=username,
                                                        login_source=login_source
                                                        )
                        data['code'] = 20603
                    user = authenticate(request=self.context.get('request'), 
                                        username=username, password=password)
                    user.save()
                    data['user'] = user 
            except MobileOTPTemp.DoesNotExist:
                MobileOTPTemp.objects.create(phone_number=phone_number, otp=otp_new)
                data['otp'] = otp_new  
                data['code'] = 20604   
            except ValueError:
                mobile_otp_obj.otp = otp_new
                mobile_otp_obj.save()
                data['otp'] = otp_new       
                data['code'] = 20604
        return data    
   
        
class FeedbackSerializer(Serializer):
    rating      = IntegerField()
    label       = CharField()
    
    def validate(self,data):
        rating      = data.get('rating')
        label       = data.get('label')
        try:
            label_obj = FeedBackLabel.objects.get(label=label)
        except:
            raise ValidationError({'ERR':'Invalid Label Type'})
        data['label']= label_obj     
        request      = self.context.get('request')
        data['user'] = request.user
        data['code'] = 20800
        return data
            
 
class OrderSerializers(Serializer):
       task_flag        = IntegerField()
       qr_code          = CharField(required=False)
       res_code         = IntegerField(required=False)
#        class Meta:
#            model = Item
#            fields = ('id', 'res_code', 'name', 'category', 'sort', 'description','type','price','task_flag','qr_code','res_code')
#        
       def validate(self,data):
            task_flag       = data.get('task_flag')
            qr_code         = data.get('qr_code')
            res_code        = data.get('res_code')
            if task_flag==1:
                try:
                    qr_obj       = QRCode.objects.get(qr_code=qr_code)
                    if qr_obj.active:
                        data['code'] = 20101
                        data['order_code'] = qr_obj.order_code
                        data['res_code'] = qr_obj.res_code
                        data['active'] = qr_obj.active
                    else:
                        data['code'] = 20102
                        data['active'] = qr_obj.active
                        qr_obj.active=1
                        qr_obj.save()
                except QRCode.DoesNotExist:
                    raise ValidationError({'code':20100})
            return data   

        
class TableFlagSerializer(Serializer):
    task_flag        = IntegerField()
    order_code       = IntegerField(required=False)
    
    def validate(self,data):
        task_flag       = data.get('task_flag')
        order_code      = data.get('order_code')
        if task_flag==1:
            data['code']=20201
        if task_flag==2:
            data['code']=20202
        return data


class TableGenerationSerializer(Serializer):
    task_flag        = IntegerField()
    res_code         = IntegerField(required=False)
    
    def validate(self,data):
        task_flag       = data.get('task_flag')
        res_code        = data.get('res_code')
        if task_flag==0:
            data['code']=20900
        elif task_flag==1:
            data['code']=20901
        return data


class QRDetailSerializer(Serializer):
    res_code         = IntegerField()
    
    def validate(self, data):
        res_code        = data.get('res_code')
        data['code'] = 20700
        return data

class OTPSerializer(Serializer):
    phone_number    = CharField()
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        new_otp      = random.randint(100000,999999)
        try:
            mobile_otp_obj = MobileOTPTemp.objects.get(phone_number=phone_number)
            mobile_otp_obj.otp = new_otp
            data['code'] = 21100
            mobile_otp_obj.save()
        except:
            MobileOTPTemp.objects.create(phone_number=phone_number, otp=new_otp)    
            data['code']=21101
        data["new_otp"] = new_otp
        return data