from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response


class UserRegistration(APIView):
    def post(self,request):
        data = UserRegistrationSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_200_OK,data={"message":"User Created Succesfully"})
        print(data.errors)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"message":"Please try later"})


def user_login(self,request):
    pass

def user_logout(self,request):
    pass
