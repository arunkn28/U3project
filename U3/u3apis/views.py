from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict

from .serializers import *
from .models import *


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_class = (AllowAny,)
    
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user:
                token, created = Token.objects.get_or_create(user=user)
                data = {
                        'code':serializer.validated_data['code'],
                        'userid' : user.id,
                        'username' : serializer.validated_data['username'],
                        'token' : token.key
                    }
            else:
                data = {
                        'code':serializer.validated_data['code'],
                        'otp':serializer.validated_data['otp']
                    }
            return Response(data=data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

class FeedbackView(APIView):
    serializer_class = FeedbackSerializer
    
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user    = serializer.validated_data['user']
            rating  = serializer.validated_data['rating']
            label   = serializer.validated_data['label']
            Rating.objects.create(user=user,label=label, rating=rating)
            data = {
                    'code':serializer.validated_data['code']
                }
            return Response(data=data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class OrderView(APIView):
    serializer_class = OrderSerializers
    
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            task_flag = serializer.validated_data['task_flag']
            if task_flag==1:
                active = serializer.validated_data['active']
                if active:
                    res_code = serializer.validated_data['res_code']
                    #res_code = serializer.validated_data['res_code']
                    res_details = ResDetails.objects.get(id=res_code.id)
                    rest_details_dict={}
                    rest_details_dict['res_code'] = res_details.id
                    rest_details_dict['res_name'] = res_details.res_name
                    rest_details_dict['res_address'] = res_details.res_address
                    items = Item.objects.filter(res_code=res_code)
                    item_list=[]
                    for item in items:
                        temp_item_dict=model_to_dict(item)
                        category = item.category
                        category_details = Category.objects.get(id=category.id)
                        temp_item_dict['category_name'] = category_details.name
                        temp_item_dict['category_sort'] = category_details.sort
                        item_list.append(temp_item_dict)
                    data = {
                            'res_details' : rest_details_dict,
                            'item_list' : item_list,
                            'code' : serializer.validated_data['code'],
                            'order_code' : serializer.validated_data['order_code']
                        }
                    return Response(data=data, status=HTTP_200_OK)
                else:
                    #pending for non active stages
                    return Response(data={'have to do':'Yes'}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
                    
                    
class TableFlagView(APIView):
    serializer_class =TableFlagSerializer
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            task_flag = serializer.validated_data['task_flag']
            order_code = serializer.validated_data['order_code']
            code = serializer.validated_data['code']
            if task_flag==1:
                QRCode.objects.filter(order_code=order_code).update(waiter=1)
            elif task_flag==2:
                QRCode.objects.filter(order_code=order_code).update(waiter=0)
            data = {
                    'code' : code
                    }
            return Response(data=data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    
class TableGenerationView(APIView):
    serializer_class =TableGenerationSerializer
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            task_flag = serializer.validated_data['task_flag']
            res_code = serializer.validated_data['res_code']
            code = serializer.validated_data['code']
            if task_flag==0:
                tables = Table.objects.filter(res_code=res_code)
                table_list=[]
                for table in tables:
                    temp_table_dict=model_to_dict(item)
                    table_list.append(temp_table_dict)
                data = {
                    'code' : code,
                    'table_list' : table_list
                    }
            elif task_flag==1:
                Table.objects.filter(res_code=res_code).delete()
                data ={
                        'code' : code
                    }
            return Response(data=data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class QRDetaiView(APIView):
    serializer_class = QRDetailSerializer
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            res_code = serializer.validated_data['res_code']
            qr_details = QRCode.objects.filter(res_code=res_code)
            code = serializer.validated_data['code']
            table_list=[]
            for qr_detail in qr_details:
                temp_table_dict=model_to_dict(qr_detail)
                table_list.append(temp_table_dict)
            data = {
                    'code' : code,
                    'table_list' : table_list
                    }
            return Response(data=data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class OTPView(APIView):
    serializer_class = OTPSerializer
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            data = {
                'code' : serializer.validated_data['code'],
                'new_otp' : serializer.validated_data['new_otp'],
                }
            return Response(data=data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

    
    
             