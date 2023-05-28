from django.contrib import admin
from .models import UserPost,PostLocation,Image,MainPlace

# Register your models here.
admin.site.register(MainPlace)
admin.site.register(Image)
admin.site.register(UserPost)
admin.site.register(PostLocation)
