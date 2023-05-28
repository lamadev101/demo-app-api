from rest_framework import serializers
from .models import PostLocation,UserPost,MainPlace,Package,PackagePlace
# from django.contrib.gis.geos import Point
from django.contrib.auth.models import User




class PostLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLocation
        fields = ('id','location_name','geo_location')

    # def create(self,validated_data):
    #     geo_location_data = validated_data['geo_location'].split(",")
    #     validated_data['geo_location'] = Point(float(geo_location_data[0]),float(geo_location_data[1]))
    #     return PostLocation.objects.create(**validated_data)



class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ('id','day','created_at','updated_at','user','main_place_id','package_id')

    def create(self,validated_data):
        return UserPost.objects.create(**validated_data)



class MainPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPlace
        fields = ('id','place_name')

    def create(self,validated_data):
        return MainPlace.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'user_email','user_address')



class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id','package_name')

    def create(self,validated_data):
        return Package.objects.create(**validated_data)



class PackagePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagePlace
        fields= ('id')

    def create(self,validated_data):
        return PackagePlace.objects.create(**validated_data)


