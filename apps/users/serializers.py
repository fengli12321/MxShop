

from rest_framework import serializers
from django.contrib.auth import get_user_model

import re
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE


from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # if not re.match(REGEX_MOBILE, mobile):
        #     raise serializers.ValidationError("手机号码非法")
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError("发送太频繁")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码==", help_text="验证码???")
    username = serializers.CharField(required=True, allow_blank=True, help_text="用户名", validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={"input_type": "password"},
        label="密码",
        write_only=True,
        required=True
    )

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_record = VerifyCode.objects.filter(mobile=self.initial_data["username"])
        if verify_record:
            last_record = verify_record[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
            # return code
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")