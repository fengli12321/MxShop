from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import  get_user_model
# Create your views here.
User = get_user_model()
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from random import choice

from .serializers import SmsSerializer, UserRegSerializer

from utils.yunpian import YunPian

from .models import VerifyCode

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian()
        code = self.generate_code()
        yun_pian.send_sms(code, mobile=mobile)

        verify_code = VerifyCode(code=code, mobile=mobile)
        verify_code.save()
        return Response({
            "code": code
        }, status=status.HTTP_201_CREATED)

class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = User.objects.all()