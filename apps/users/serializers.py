

from rest_framework import serializers
from django.contrib.auth import get_user_model

import re
from datetime import datetime
from datetime import timedelta

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
