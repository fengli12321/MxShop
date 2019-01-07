from django.shortcuts import render


from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your tests here.
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AdressSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly

class UserFavViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = UserFav.objects.all()
    lookup_field = "goods_id"


    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class LeavingMessageViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserLeavingMessage.objects.filter
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

class AdressViewSets(viewsets.ModelViewSet):
    serializer_class = AdressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)