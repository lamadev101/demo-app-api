from django.contrib.gis.db import models
from django.contrib.auth.models import User


#main place information top level entity to location place.
class MainPlace(models.Model):
    place_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.place_name}"


#package which holds the package information
class Package(models.Model):
    package_name = models.CharField(max_length=200,null=False)
    def __str__(self):
        return f"{self.package_name}"


#package place information  [contains unique id of main place and package]
class PackagePlace(models.Model):
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    main_place = models.ForeignKey(MainPlace,on_delete=models.CASCADE)


#model that holds the user posted information with itinerary traveled days and users id
class UserPost(models.Model):
    day = models.IntegerField(null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_place_id = models.IntegerField(null=True)
    package_id  = models.IntegerField(null= True)

    def __str__(self):
        return f"{self.id}"


#model that holds the location place information like [ Koteshwor ] which reside into  [ kathmandu ]
class PostLocation(models.Model):
    location_name  = models.CharField(max_length=200,null=False)
    geo_location = models.PointField(null=False)
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location_name}"


#models holds the image data
class Image(models.Model):
    image_post = models.ImageField(upload_to='images/',null=False)
    post_location = models.ForeignKey(PostLocation, on_delete=models.CASCADE,null=True)


